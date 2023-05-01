import dotenv
import logging

from datetime import datetime

# Importing scraping and data processing modules

from dependencies.scraping.scraper import ScraperTendersIndia
from dependencies.cleaning.cleaning import CleanerTendersIndia
from dependencies.geocoding.geocoder import GeocoderTendersIndia
from dependencies.standardization.standardizer import StandardizerTendersIndia

dotenv.load_dotenv(".env")
logging.basicConfig(level=logging.INFO)


config = {
        # path configurations
        "path_config": {
            "meta_data_path":         "../../data/meta_data.csv",
            "raw_data_path":          "../../data/raw_data.csv",
            "cleaned_data_path":      "../../data/cleaned_data.csv",
            "geocoded_data_path":     "../../data/geocoded_data.csv",
            "standardized_data_path": "../../data/standardized_data.csv",
        }
    }

# In each step create an object of the class, initialize the class with 
# required configuration and call the run method 
def step_1():
    logging.info("Meta data will be scraped with main data (step 2)")


def step_2():
    logging.info("Scraped Main Data")
    obj = ScraperTendersIndia(config=config)
    obj.run()


def step_3():
    logging.info("Cleaned Main Data")
    obj = CleanerTendersIndia(config=config)
    obj.run()


def step_4():
    logging.info("Geocoded Cleaned Data")
    obj = GeocoderTendersIndia(config=config)
    obj.run()


def step_5():
    logging.info("Standardized Geocoded Data")
    obj = StandardizerTendersIndia(config=config)
    obj.run()


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
