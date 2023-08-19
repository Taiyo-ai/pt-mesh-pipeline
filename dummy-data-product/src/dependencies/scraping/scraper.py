from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup


@dataclass
class DataScraper:
    url: str

    def scrape(self) -> BeautifulSoup:
        """Returns a beautiful soup object of the page at self.url"""

        # Send an HTTP Get request and validate the response
        response = requests.get(self.url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "lxml")
        return soup
