# import your dependencies here
import pandas as pd
import os
import spacy
from stringcase import snakecase
import numpy as np
from scipy import sparse
from dataprep.eda import create_report


class Standardizer:
    def __init__(self, **kwargs):
        self.config = kwargs.get("config")

    def load_data(self):
        """Function to load data"""

        geocoded_data_path = self.config["path_config"]["geocoded_data_path"]
        self.raw_data = pd.read_csv(geocoded_data_path + "/geocoded_data.csv")

        return None

    def standardize(self):
        """Do extraction or processing of data here"""

        def standardize_status(status):
            if status == "FINAL PAYMENT MADE":
                return "closed"
            elif status == "NTP ISSUED":
                return "prospective"
            elif status == "EXECUTED":
                return "closed"
            elif status == "FINAL ACCEPTED":
                return "closed"
            else:
                return "Not Available"

        self.raw_data["lettingDate"] = self.raw_data["lettingDate"].apply(lambda time: str(pd.Timestamp(time)).split('+')[0])          #
        self.raw_data["workBeginDate"] = self.raw_data["workBeginDate"].apply(lambda time: str(pd.Timestamp(time)).split('+')[0])          #
        self.raw_data["awardDate"] = self.raw_data["awardDate"].apply(lambda time: str(pd.Timestamp(time)).split('+')[0])            #
        self.raw_data["executedDate"] = self.raw_data["executedDate"].apply(lambda time: str(pd.Timestamp(time)).split('+')[0])         #
        self.raw_data["timeBeganDate"] = self.raw_data["timeBeganDate"].apply(lambda time: str(pd.Timestamp(time)).split('+')[0])        # Necessary Time conversion
        self.raw_data["finalAcceptedDate"] = self.raw_data["finalAcceptedDate"].apply(lambda time: str(pd.Timestamp(time)).split('+')[0])    #
        self.raw_data["startDate"] = self.raw_data["startDate"].apply(lambda time: str(pd.Timestamp(time)).split('+')[0])            #
        self.raw_data["estimatedCompletion"] = self.raw_data["estimatedCompletion"].apply(lambda time: str(pd.Timestamp(time)).split('+')[0])  #
        self.raw_data["countryCode"] = "USA"
        self.raw_data["countryName"] = "United States of America"
        self.raw_data["state"] = "Florida"
        self.raw_data["identifiedSector"] = "sco construction"
        self.raw_data["source"] = "https://scoc.fdot.gov"
        self.raw_data["augId"] = self.raw_data["source"] + "_" + self.raw_data["$id"].apply(str)
        self.raw_data["text"] = self.raw_data[["$type", "vendorName", "projectEngineerManagerName", "description", "contractTypeDescription", "minContractTypeDescription"]].agg(' '.join, axis=1)
        self.raw_data["identifiedStatus"] = self.raw_data["contractStatus"].apply(standardize_status)
        self.raw_data["map_coordinates"] = self.raw_data[["lat", "long"]].apply(tuple, axis=1)
        self.raw_data["project_or_tender"] = "P"

        modified_column_names = {}
        columns_list = list(self.raw_data)
        for column in columns_list:
            modified_column_names[column] = column
        modified_column_names["countyDescription"] = "county"
        modified_column_names["letingDate"] = "bidOpeningDate"
        modified_column_names["$id"] = "originalId"
        modified_column_names["contractName"] = "name"
        modified_column_names["projectMixDescription"] = "description"
        modified_column_names["active"] = "status"
        modified_column_names["categoryDescription"] = "budget"
        modified_column_names["mapUrl"] = "url"
        for key, value in modified_column_names.items():  # Dictionary for renaming the fields
            modified_column_names[key] = snakecase(value)

        self.raw_data.rename(columns=modified_column_names, inplace=True)  # Renaming According to naming conventions
        self.raw_data.drop(columns=["unnamed:_0_1", "unnamed:_0"], inplace=True)
        self.raw_data = self.raw_data.fillna(np.NaN)

        nlp = spacy.load("en_core_web_trf")
        self.raw_data["keywords"] = self.raw_data["text"].apply(lambda t: nlp(t).ents)

        return None

    def save_data(self):
        """Function to save data"""

        standardized_data_path = self.config["path_config"]["standardized_data_path"]
        self.raw_data.to_csv(standardized_data_path + "/standardized_data.csv")

        return None

    def run(self):
        """Load data, do_something and finally save the data"""

        self.load_data()
        self.standardize()
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

    obj = Standardizer(config=config)
    obj.run()
