import dotenv
import logging
# import os

from datetime import datetime

# Importing scraping and data processing modules
from dependencies.scraping.scraper import TexasScraper
from dependencies.cleaning.cleaning import TexasCleaner
from dependencies.geocoding.geocoder import TexasGeocoder
from dependencies.standardization.standardizer import TexasStandardizer
# from dependencies.utils import get_path

dotenv.load_dotenv(".env")
logging.basicConfig(level=logging.INFO)


# In each step create an object of the class, initialize the class with
# required configuration and call the run method
def step_1():
    scraper_object = TexasScraper()
    scraper_object.run()
    logging.info("Scraped Main Data")


def step_2():
    cleaner_object = TexasCleaner()
    cleaner_object.run()
    logging.info("Cleaned Main Data")


def step_3():
    geocoder_object = TexasGeocoder()
    geocoder_object.run()
    logging.info("Geocoded Cleaned Data")


def step_4():
    standardizer_object = TexasStandardizer()
    standardizer_object.run()
    logging.info("Standardized Geocoded Data")


def step_5():
    logging.info("")


if __name__ == "__main__":
    import argparse
    dotenv.load_dotenv()

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
