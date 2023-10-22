import requests
from bs4 import BeautifulSoup
import csv

class TenderScraper:
    def __init__(self, url):
        self.url = url

    def scrape(self):
        # Updated scraping logic
        # Your code to extract tenders from the chosen source
        pass

if __name__ == "__main__":
    # Example usage:
    world_bank_url = "https://ieg.worldbankgroup.org/data"
    scraper = TenderScraper(world_bank_url)
    scraper.scrape()
