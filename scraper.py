# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 10:50:32 2023

@author: GKumar
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup
import logging
import os

class TenderScraper:
    def __init__(self):
        self.url = "https://etenders.gov.in/eprocure/app"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"}
        self.soup = None
        self.logger = logging.getLogger(__name__)
        self.output_file = os.environ.get("OUTPUT_FILE", "tender_data.csv")

    def get_data(self):
        self.logger.info("Making a GET request to %s", self.url)
        response = requests.get(self.url, headers=self.headers)
        self.soup = BeautifulSoup(response.text, "html.parser")
        table = self.soup.find("table", class_="tenders-table")
        table_rows = table.tbody.find_all("tr")
        data = []
        for tr in table_rows:
            td = tr.find_all("td")
            row = [tr.text.strip() for tr in td if tr.text.strip()]
            if row:
                data.append(row)
        df = pd.DataFrame(data, columns=["Tender Reference Number", "Department Name", "Organization", "Tender Title",
                                         "Publish Date", "Due Date", "Status"])
        self.logger.info("Saving data to %s", self.output_file)
        df.to_csv(self.output_file, index=False)

def main():
    scraper = TenderScraper()
    scraper.get_data()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
