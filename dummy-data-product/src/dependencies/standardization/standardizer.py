import pandas as pd
import re
import pycountry
pd.options.display.max_columns = None
pd.options.display.max_rows = None

class StandardizerTendersIndia:
    def __init__(self, **kwargs):
        self.config = kwargs.get("config")

        self.data_dir = "../../../../data"

        self.meta_df = None
        self.df = None


    def get_country_code_alpha3(self, e):
        if pd.isna(e): return e
        res = pycountry.countries.get(alpha_2=e).alpha_3

        return res


    def do_something(self):
        """Do extraction or processing of data here"""

        ## convert column names to snake case for meta data
        self.meta_df.columns = [ re.sub( r"\-|\s+", "_", e.strip().lower()) for e in self.meta_df.columns  ]

        ## convert column names to snake case for main data
        self.df.columns = [ re.sub( r"\-|\s+", "_", e.strip().lower()) for e in self.df.columns  ]

        ## standard country code
        self.df["country_code"] = self.df["country_code_2"].apply(lambda x: self.get_country_code_alpha3(x) )

               
        # conversion to datetime 
        self.df["e_published_date"] = pd.to_datetime(self.df["e_published_date"], format="%d-%b-%Y%I:%M%p").dt.tz_localize("Asia/Kolkata")
        self.df["closing_date"] = pd.to_datetime(self.df["closing_date"], format="%d-%b-%Y%I:%M%p").dt.tz_localize("Asia/Kolkata")
        self.df["opening_date"] = pd.to_datetime(self.df["opening_date"], format="%d-%b-%Y%I:%M%p").dt.tz_localize("Asia/Kolkata")
        
        ## standard utc timezone
        self.df["e_published_date"] = self.df["e_published_date"].dt.tz_convert("UTC")
        self.df["closing_date"] = self.df["closing_date"].dt.tz_convert("UTC")
        self.df["opening_date"] = self.df["opening_date"].dt.tz_convert("UTC")

        #print(self.df.head())

        return None

    def load_data(self):
        """Function to load data"""
        self.df = pd.read_csv(self.config["path_config"]["geocoded_data_path"])
        #print(self.df)

        self.meta_df = pd.read_csv(self.config["path_config"]["meta_data_path"])
        #print(self.meta_df)

        return None

    def save_data(self):
        """Function to save data"""

        ## save standardized main data
        self.df.to_csv(self.config["path_config"]["standardized_data_path"], index=False)

        ## save standardized meta data
        self.meta_df.to_csv(self.config["path_config"]["meta_data_path"], index=False)

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
    obj = StandardizerTendersIndia(config = config)
    obj.run()