from datetime import datetime


class InMemoryLogger:
    """
    A simple logger that stores logs in memory.
    """

    def __init__(self):
        self.logs = []

    def log(self, message):
        """
        Log a message with a timestamp.
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"
        self.logs.append(formatted_message)
        print(formatted_message)  # Optionally print to console

    def get_logs(self):
        """
        Retrieve all logged messages.
        """
        return "\n".join(self.logs)

    def clear_logs(self):
        """
        Clear all logs.
        """
        self.logs.clear()

    def save_to_file(self, filename="log.txt"):
        """
        Save logs to a text file.
        """
        with open(filename, "w") as file:
            file.write(self.get_logs())
        print(f"Logs saved to {filename}")
