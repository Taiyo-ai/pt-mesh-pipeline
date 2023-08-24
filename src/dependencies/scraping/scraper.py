
import requests
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self, config):
        self.config = config
        self.url = config["scraper"]["url"]  # Example: "https://example.com"

    def do_something(self):
        """Do scraping of data here"""
        response = requests.get(self.url)
        if response.status_code == 200:
            content = response.content
            return content
        else:
            print(f"Failed to fetch data from {self.url}")
            return None

    def run(self):
        raw_data = self.do_something()
        return raw_data
