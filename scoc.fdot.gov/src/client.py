import os
import dotenv
import logging
from datetime import datetime

# Importing scraping and data processing modules
from dependencies.scraping.scraper import Scraper
from dependencies.scraping.meta_scraper import metaScraper
from dependencies.cleaning.cleaning import Cleaner
from dependencies.geocoding.geocoder import Geocoder
from dependencies.standardization.standardizer import Standardizer

dotenv.load_dotenv(".env")
logging.basicConfig(level=logging.INFO)
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
# In each step create an object of the class, initialize the class with
# required configuration and call the run method

def step_1():
    obj = metaScraper(config=config)
    obj.run()
    logging.info("Standardized Geocoded Data")

def step_2():
    obj = Scraper(config=config)
    obj.run()
    logging.info("Scraped Metadata")


def step_3():
    obj = Cleaner(config=config)
    obj.run()
    logging.info("Scraped Main Data")

def step_4():
    obj = Geocoder(config=config)
    obj.run()
    logging.info("Cleaned Main Data")

def step_5():
    obj = Standardizer(config=config)
    obj.run()
    logging.info("Geocoded Cleaned Data")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--step", help="step to be choosen for execution")

    args = parser.parse_args()

    eval(f"step_{args.step}()")

    logging.info(
        {
            "last_executed": str(datetime.now()),
            "status": "Pipeline executed successfully",
        }
    )
