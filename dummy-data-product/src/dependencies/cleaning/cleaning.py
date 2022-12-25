import pandas as pd
import logging
from dependencies.utils import get_path


class TexasCleaner:

    def __init__(self) -> None:
        self.df = None

    def load_data(self):
        self.df = pd.read_csv(get_path("master_data_path"), keep_default_na=False, index_col=0)

    def process(self):
        self.df["country_name"] = "United States of America"
        self.df["country_code"] = "USA"
        self.df["region_name"] = "North America"
        self.df["region_code"] = "NAC"
        self.df["unit"] = "Dollar"
        self.df.drop_duplicates(inplace=True)

    def save_data(self):
        self.df.to_csv(get_path("cleaned_data_path"))

    def run(self):
        logging.info("Cleaning Started")
        self.load_data()
        self.process()
        self.save_data()
        logging.info("Cleaning Done")


if __name__ == "__main__":
    # Example configuration dictionary
    config = {
        # class specific configuration
        "webdriver_path": "path_to_webdriver",
        "PROCESSES": 15,

        # path configurations
        "path_config": {
            "meta_data_path": "rel_path",
            "raw_data_path": "rel_path",
            "cleaned_data_path": "rel_path",
            "geocoded_data_path": "rel_path",
            "standardized_data_path": "rel_path",
        }
    }
    obj = TexasCleaner(config=config)
    obj.run()
