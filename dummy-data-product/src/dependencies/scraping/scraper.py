# Web SCrapper class to get data from set URL in .env

from bs4 import BeautifulSoup
import requests
import csv
import logging
# import os,sys
# from datetime import datetime


class WebScrapper:
    def __init__(self, URL, file_name=None):

        logging.info("WebScraper class called")
        self.URL = URL
        self.file_name = "main_data.csv"

    # Run function to scrape and save data from URL
    def run(self):

            response = requests.get(self.URL)
            print("Inside run")
            if response.status_code == 200:

                logging.info(f"Connected to {self.URL} ,status code : {response.status_code}")
                r=response.text
                soup = BeautifulSoup(response.text, 'html.parser')

                with open(f"<>pt-mesh-pipeline-main\\data\\main_data\\{self.file_name}", mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)

                    # Writing headerss
                    head_row = ['Tender Title', 'Reference No', 'Closing Date', 'Bid Opening Date']
                    writer.writerow(head_row)

                    tender_tables = soup.find_all('table', id='activeTenders')
                    for table in tender_tables:
                        tender_data = self.data_extraction(table)
                        writer.writerows(tender_data)



    def data_extraction(self, table_element):
        data_rows = []
        rows = table_element.find_all('tr', class_=["even", "odd"])

        for row in rows:
            row_data = []
            cols = row.find_all('td')
            for col in cols:
                col_text = col.get_text(strip=True)
                row_data.append(col_text)
            data_rows.append(row_data)

        return data_rows
