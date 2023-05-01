import pandas as pd
import re
import pgeocode
pd.options.display.max_columns = None
pd.options.display.max_rows = None


class GeocoderTendersIndia:
    def __init__(self, **kwargs):
        self.config = kwargs.get("config")

        self.data_dir = "../../../../data"

        self.df = None

    def do_something(self):
        """Do extraction or processing of data here"""
        nomi = pgeocode.Nominatim('IN')

        ## pincode => details dict
        geocode_details = {}
        for e in self.df["pincode"].unique():
            geocode_details[e] =  nomi.query_postal_code(str(e)).to_dict()

        self.df["location_longitude"] = self.df["pincode"].apply(lambda x: geocode_details[x]["longitude"])
        self.df["location_latitude"] = self.df["pincode"].apply( lambda x: geocode_details[x]["latitude"])

        self.df["region_name"] = self.df["pincode"].apply( lambda x: geocode_details[x]["community_name"] )
        self.df["region_code"] = self.df["pincode"].apply( lambda x: geocode_details[x]["community_code"])
        self.df["country_name"] = "India"
        self.df["country_code_2"] = self.df["pincode"].apply( lambda x: geocode_details[x]["country_code"])
        
        self.df["state"] = self.df["pincode"].apply( lambda x: geocode_details[x]["state_name"])
        self.df["county"] = self.df["pincode"].apply( lambda x: geocode_details[x]["county_name"])
        self.df["city"] = self.df["pincode"].apply( lambda x: geocode_details[x]["place_name"])
        self.df["map_coordinates"] = self.df["pincode"].apply( lambda x: (geocode_details[x]["latitude"], geocode_details[x]["longitude"] ) )

        #print(self.df.head())

        return None

    def load_data(self):
        """Function to load data"""
        
        self.df = pd.read_csv(self.config["path_config"]["cleaned_data_path"])

        return None

    def save_data(self):
        """Function to save data"""

        ## save geocoded data
        self.df.to_csv(self.config["path_config"]["geocoded_data_path"], index=False)

        return None

    def run(self):
        """Load data, do_something and finally save the data"""

        self.load_data()

        self.do_something()

        self.save_data()

        return None


if __name__ == "__main__":
    # Example configuration dictionary
    config = {
        # path configurations
        "path_config": {
            "meta_data_path": "../../../../data/meta_data.csv",
            "raw_data_path": "../../../../data/raw_data.csv",
            "cleaned_data_path": "../../../../data/cleaned_data.csv",
            "geocoded_data_path": "../../../../data/geocoded_data.csv",
            "standardized_data_path": "../../../../data/standardized_data.csv",
        }
    }
    obj = GeocoderTendersIndia(config = config)
    obj.run()