# import your dependencies here
import pandas as pd
import os
import numpy as np


class Cleaner:
    def __init__(self, **kwargs):
        self.config = kwargs.get("config")

    def load_data(self):
        """Function to load data"""

        self.raw_data_path = self.config["path_config"]["raw_data_path"]
        self.raw_data = pd.read_csv(self.raw_data_path + "/raw_data.csv")
        self.cleaned_data_path = self.config["path_config"]["cleaned_data_path"]

        return None

    def clean_and_modify(self):
        """Do extraction or processing of data here"""

        self.raw_data = self.raw_data.fillna(np.NaN)  # fill the missing or null values with NA(Not Applicable)
        self.raw_data.drop_duplicates()  # drop the duplicates

        return None

    def save_data(self):
        """Function to save data"""

        self.raw_data.to_csv(self.cleaned_data_path + "/cleaned_data.csv")

        return None

    def run(self):
        """Load data, do_something and finally save the data"""

        self.load_data()
        self.clean_and_modify()
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
            "meta_data_path": "rel_path",
            "raw_data_path": os.getcwd() + "/data/raw_data",
            "cleaned_data_path": os.getcwd() + "/data/cleaned_data",
            "geocoded_data_path": os.getcwd() + "/data/geocoded_data",
            "standardized_data_path": os.getcwd() + "/data/standardized_data",
        }
    }

    # print(config["path_config"]["cleaned_data_path"])
    # print(config["path_config"]["raw_data_path"])

    obj = Cleaner(config=config)
    obj.run()
