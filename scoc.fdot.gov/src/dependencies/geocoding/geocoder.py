# import your dependencies here
import pandas as pd
import os
from geopy.geocoders import Nominatim


class Geocoder:
    def __init__(self, **kwargs):
        self.config = kwargs.get("config")

    def load_data(self):

        cleaned_data_path = self.config["path_config"]["cleaned_data_path"]
        self.raw_data = pd.read_csv(cleaned_data_path + "/cleaned_data.csv")
        # self.raw_data = pd.read_csv("/home/dips/Desktop/rdata.csv")

        return None

    def geolocate(self):
        """Do extraction or processing of data here"""

        self.raw_data["countyDescription"] = self.raw_data["countyDescription"].str.replace("MIAMI-DADE", "MIAMI")
        self.raw_data["fullAddress"] = self.raw_data["countyDescription"] + ", FL, US"

        geolocator = Nominatim(timeout=10, user_agent="myGeolocator")
        self.raw_data["gcode"] = self.raw_data["fullAddress"].apply(geolocator.geocode)
        self.raw_data.at[4, "gcode"] = None

        self.raw_data["lat"] = self.raw_data["gcode"].apply(lambda loc: loc.latitude if loc else "NA")    # Latitude
        self.raw_data["long"] = self.raw_data["gcode"].apply(lambda loc: loc.longitude if loc else "NA")  # Longitude

        return None

    def save_data(self):
        """Function to save data"""

        geocoded_data_path = self.config["path_config"]["geocoded_data_path"]
        self.raw_data.to_csv(geocoded_data_path + "/geocoded_data.csv")

        return None

    def run(self):
        """Load data, do_something and finally save the data"""

        self.load_data()
        self.geolocate()
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

    obj = Geocoder(config=config)
    obj.run()
