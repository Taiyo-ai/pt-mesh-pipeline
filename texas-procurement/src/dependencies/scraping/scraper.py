import pandas as pd
import logging
from dependencies.utils import get_path


class TexasScraper:

    def __init__(self) -> None:
        self.df = None

    def load_data(self):
        self.df = pd.read_excel("ftp://ftp.dot.state.tx.us/pub/txdot-info/tpp/project-tracker/Project_Tracker.xls", engine="xlrd")

    def process(self):
        column_list = self.df.iloc[4].values.flatten().tolist()
        self.df.columns = column_list
        self.df = self.df.iloc[5:]

    def save_data(self):
        self.df.to_csv(get_path("master_data_path"))

    def run(self):
        logging.info("Scraping Started")
        self.load_data()
        self.process()
        self.save_data()
        logging.info("Scraping Done")


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
    obj = TexasScraper(config=config)
    obj.run()
