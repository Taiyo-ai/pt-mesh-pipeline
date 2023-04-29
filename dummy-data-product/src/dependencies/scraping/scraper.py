import requests
import os

import numpy as np
import pandas as pd

import time
import json

##Web Scraping Library
from selenium import webdriver
from bs4 import BeautifulSoup

class Web_Scraping:
    def __init__(self, url, table_columns):
        self.url = url
        self.table_columns = table_columns

    def scrape_data(self):
        active_data = []
        df = pd.DataFrame(active_data, columns=self.table_columns)
        page = requests.get(self.url)
        
        ##Html parser
        ##BeautifulSoup used for parsing
        soup = BeautifulSoup(page.content, 'html.parser')
        tenders = soup.find_all('table',{'id': 'activeTenders'})
        index = 0
        for row in tenders[0].find_all('tr'):
            col = 0
            column = row.find_all('td')
            for x in column:
                df.loc[index, self.table_columns[col]] = x.get_text()
                col = col + 1
            index = index + 1
        # Store to csv file
        df.to_csv('ActiveTender.csv', index=False)

if __name__ == '__main__':
    url = 'https://etenders.gov.in/eprocure/app'
    table_columns = ['Tender Title', 'Reference No', 'Closing Date', 'Bid Opening Date']
    scrape = Web_Scraping(url, table_columns)
    scrape.scrape_data()

##df=pd.read_csv("ActiveTender.csv",encoding= 'unicode_escape')
##df.head(2)
