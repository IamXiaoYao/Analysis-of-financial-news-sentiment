# News Crawler and Sentiment Analysis
This project consists of two primary components: a news crawler for scraping Yahoo Finance articles and a sentiment analysis pipeline for processing and analyzing the sentiment of the articles. These tools are designed to streamline the data collection and analysis process for financial news.
## Features
### 1. Yahoo News Crawler (yahoo_news_crawler.py)
Description: A Python script leveraging Selenium to scrape financial news articles from Yahoo Finance.
Key Features:
Extracts titles, links, publication times, and content of the articles.
Saves the scraped data in a structured format (CSV).
Utilizes logging to monitor the scraping process.
Dependencies:
<li>selenium</li>
<li>lxml</li>
<li>pandas</li>
<li>asyncio</li>

### 2. Sentiment Analysis (sentiment_analysis.ipynb)
Description: A Jupyter Notebook that processes the scraped news articles and evaluates their sentiment using pre-trained NLP models.
Key Features:
Utilizes the Hugging Face transformers library for sentiment classification.
Processes news articles to classify sentiments as positive, negative, or neutral.
Displays results with visualizations and statistics for insights.
Dependencies:
<li>transformers</li>
<li>pandas</li>
<li>tqdm</li>
<li>scipy</li>

## Getting Started
If you're new, begin by running the crawler to gather data, and then explore the sentiment analysis notebook to uncover insights. Every great project begins with a simple first step—get started now!

## Show Your Support ⭐
If you found this project helpful, don’t forget to give it a star on GitHub! It helps others discover the project and motivates us to keep improving and adding new features. Thank you for your support! 😊
