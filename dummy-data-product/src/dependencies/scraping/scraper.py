from dataclasses import dataclass

import requests
from requests import Response

from bs4 import BeautifulSoup


@dataclass
class DataScraper:
    url: str

    @staticmethod
    def get_confirmed_response(url: str) -> "Response":
        # Send an HTTP Get request and validate the response
        session = requests.Session()
        # Set user-agent header to mimic a browser
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        session.headers["User-Agent"] = user_agent

        response = session.get(url)
        response.raise_for_status()

        if "Your session has timed out." in response.text:
            _ = session.get("https://etenders.gov.in/eprocure/app?service=restart")
            response = session.get(url)
            response.raise_for_status()

        return response

    @staticmethod
    def filter(soup: BeautifulSoup):
        ...

    def scrape(self) -> BeautifulSoup:
        """Returns a beautiful soup object of the page at self.url"""
        response = self.get_confirmed_response(self.url)
        soup = BeautifulSoup(response.text, "lxml")
        return soup
