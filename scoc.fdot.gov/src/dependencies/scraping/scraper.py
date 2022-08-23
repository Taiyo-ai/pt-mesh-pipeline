# import your dependencies here
import requests
import csv
import os
import json
from stringcase import snakecase


class Scraper:
    def __init__(self, **kwargs):
        self.config = kwargs.get("config")

    def load_data(self):
        """Function to load data"""

        url = self.config["webdriver_path"]
        self.json_response = requests.get(url).json()

        return None

    def prepare_csv_data(self):
        """Do extraction or processing of data here"""

        self.fields = []
        self.field_json = {}
        for key in self.json_response[0].keys():
            self.fields.append(key)
            self.field_json[key] = snakecase(key)

        self.raw_data_file_path = self.config["path_config"]["raw_data_path"] + "/raw_data.csv"
        self.json_file_path = self.config["path_config"]["raw_data_path"] + "/raw_data.json"

        return None

    def save_data(self):
        """Function to save data"""

        with open(self.json_file_path, 'w') as jfile:
            json.dump(self.json_response, jfile)

        with open(self.raw_data_file_path, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fields)
            writer.writeheader()
            writer.writerows(self.json_response)

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
    obj = Scraper(config=config)
    obj.run()
