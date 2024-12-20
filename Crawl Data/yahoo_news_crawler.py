import asyncio
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import Log
import pandas as pd
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Initialize logger
logger = Log.InMemoryLogger()

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)


async def get_page_source(url, driver_path):
    """
    Args:
        url (str): The URL of the webpage to fetch.
        driver_path (str, optional): Path to the ChromeDriver. Defaults to None (auto-detect if in PATH).

    Returns:
        str: The page source of the loaded webpage.
    """
    logger.log(f"Initializing WebDriver for URL: {url}")
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        # Initialize the WebDriver
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service, options=options)
        # Open Yahoo Finance Tesla News page
        try:
            await loop.run_in_executor(executor, driver.get, url)
            logger.log(f"Page loaded for: {url}")
            # Scroll down to load additional content
            for i in range(3):  # Adjust the number of scrolls as needed
                logger.log(f"Scrolling down ({i + 1}/3) for: {url}")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                await asyncio.sleep(2)  # Wait for content to load

            # Find the parent section by class name
            parent_class = "news-stream"
            child_class = "holder"
            try:
                parent_section = driver.find_element(By.CLASS_NAME, parent_class)
                child_section = parent_section.find_element(By.CLASS_NAME, child_class)
                logger.log(f"HTML content extracted for: {url}")
                return child_section.get_attribute("outerHTML")
            except Exception:
                logger.log(f"Error extracting content for {url}: {e}")
                return None
        finally:
            driver.quit()


async def parse_data(url, driver_path="/usr/local/bin/chromedriver"):
    """
    Parse the HTML content to extract news data.
    """
    logger.log(f"Starting data parsing for URL: {url}")
    html_text = await get_page_source(url, driver_path)
    if not html_text:
        return []

    dom = etree.HTML(html_text)
    list_items = dom.xpath("//li")
    news_lists = []
    for li in list_items:
        # Check if the <li> contains <span>Ad</span>
        ad_span = li.xpath(".//span[text()='Ad']")
        if ad_span:
            continue
        # title
        title = li.xpath(".//div[contains(@class, 'content')]//a/@title")
        # link
        link = li.xpath(".//div[contains(@class, 'content')]//a/@href")
        # content
        content = li.xpath(".//div[contains(@class, 'content')]//p/text()")
        # (time published)
        footer = li.xpath(
            ".//div[contains(@class, 'footer')]//i/following-sibling::text()"
        )

        if title and link and content:
            news_list = {
                "title": title[0] if title else "No Title",
                "link": link[0] if link else "No Link",
                "content": content[0].strip() if content else "No Content",
                "release_time": footer[0].strip() if footer else "No Time Info",
            }
            news_lists.append(news_list)
    logger.log(f"Data parsing complete for URL: {url}. {len(news_lists)} items found.")
    return news_lists


async def fetch_all_data(urls, driver_path="/usr/local/bin/chromedriver"):
    """
    Fetch data concurrently for all URLs.
    """
    logger.log("Starting data fetching for all URLs...")
    tasks = [parse_data(url, driver_path) for url in urls]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    data = []
    for result in results:
        if isinstance(result, list):  # Valid data
            data.extend(result)
        else:  # Handle exceptions
            print(f"Error fetching data: {result}")
    logger.log("Data fetching complete for all URLs.")
    return data


def SaveExcel(data, filename):
    """
    Save the data to a CSV file.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename_with_time = f"{filename}_{timestamp}.csv"
    df = pd.DataFrame(data)
    df.columns = [str(col).upper() for col in df.columns]
    df.to_csv(filename_with_time)
    logger.log(f"Data saved to {filename_with_time}")


if __name__ == "__main__":
    file_name = "yahoo_news"
    c_name = ["TSLA", "RKLB", "RGTI", "NVDA"]
    urls = [f"https://finance.yahoo.com/quote/{name}/latest-news/" for name in c_name]
    try:
        logger.log("Starting the program...")
        print("Fetching data...")
        flattened_data = asyncio.run(fetch_all_data(urls))
        SaveExcel(flattened_data, file_name)
        logger.log("Process completed successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

    log_filename = "process_log.txt"
    logger.save_to_file(log_filename)
