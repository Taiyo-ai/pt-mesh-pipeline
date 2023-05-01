import pandas as pd
import re

from currency_converter import CurrencyConverter

pd.options.display.max_columns = None
pd.options.display.max_rows = None

class CleanerTendersIndia:
    def __init__(self, **kwargs):
        self.config = kwargs.get("config")
        self.data_dir = "../../../../data"

        self.df = None

    def do_something(self):
        """Do extraction or processing of data here"""
        df_tmp = self.df["Title and Ref.No./Tender ID"].str.split(']', n=2, expand=True)
        df_tmp.columns = ["title", "ref_no", "tender_id"]

        regex_pat = re.compile(r'\[|\]')
        for col in df_tmp.columns:
            df_tmp[col] = df_tmp[col].str.replace(regex_pat, "", regex=True)

        ## add new columns in main data
        for col in df_tmp.columns:
            self.df[col] = df_tmp[col]

        ## drop old column
        self.df.drop(columns=["Title and Ref.No./Tender ID"], inplace=True)

        ### convert tender value to usd
        c = CurrencyConverter()
        self.df["tender_value_usd"] = self.df["tender_value_inr"].apply( lambda amt: c.convert(amt, 'INR', 'USD') )

        return None

    def load_data(self):
        """Function to load data"""
        
        self.df = pd.read_csv(self.config["path_config"]["raw_data_path"])

        return None

    def save_data(self):
        """Function to save data"""

        ## save cleaned data
        self.df.to_csv(self.config["path_config"]["cleaned_data_path"], index=False)

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
    obj = CleanerTendersIndia(config = config)
    obj.run()