from importlib.resources import contents
from re import M, S
from bs4 import BeautifulSoup
import requests
import csv
import os
from pathlib import Path
import json
from stringcase import snakecase

class metaScraper:
    def __init__(self, **kwargs):
        self.config = kwargs.get("config")

    def load_data(self):
        """Function to load data"""

        url = "https://scoc.fdot.gov/"
        self.json_response = requests.get(url).text

        return None

    def prepare_csv_data(self):
        """Do extraction or processing of data here"""

        soup = BeautifulSoup(self.json_response, 'lxml')
        self.metas = soup.find_all('meta')
        self.meta_data_path = self.config["path_config"]["meta_data_path"] + "/meta_data.txt"

        return None

    def save_data(self):
        """Function to save data"""
        print(self.meta_data_path)

        with open(self.meta_data_path, 'w') as jfile:
            for meta in self.metas:
                jfile.writelines(str(meta) + "\n")

        return None

    def run(self):
        """Load data, do_something and finally save the data"""
        self.load_data()
        self.prepare_csv_data()
        self.save_data()

        return None


if __name__ == "__main__":
    # Example configuration dictionary
    config = {
        # class specific configuration
        "webdriver_path": "https://scoc.fdot.gov/api/ActiveContract/GetContracts",
        "PROCESSES": 15,

        # path configurations

        "path_config": {
            "meta_data_path": os.getcwd() + "/data/meta_data",
            "raw_data_path": os.getcwd() + "/data/raw_data",
            "cleaned_data_path": os.getcwd() + "/data/cleaned_data",
            "geocoded_data_path": os.getcwd() + "/data/geocoded_data",
            "standardized_data_path": os.getcwd() + "/data/standardized_data",
        }
    }
    obj = metaScraper(config=config)
    obj.run()
