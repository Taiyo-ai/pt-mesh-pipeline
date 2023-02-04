import dotenv
import logging

from datetime import datetime

import sys
sys.path.insert(0, '/Users/Dell/Documents/My Files/TaiyoAI/pt-mesh-pipeline/dummy-data-product/src/')

# Importing scraping and data processing modules
from dependencies.scraping.etenders_scraper import scrape_etender_data
from dependencies.scraping.chinabidding_scraper import scrape_chinabidding_data
# from dependencies.cleaning.<file_name> import <class_name>
# from dependencies.geocoding.<file_name> import <class_name>
# from dependencies.standardization.<file_name> import <class_name>

dotenv.load_dotenv(".env")
logging.basicConfig(level=logging.INFO)


# In each step create an object of the class, initialize the class with 
# required configuration and call the run method 
def step_1():
    scrape_etender_data()
    scrape_chinabidding_data()
    logging.info("Scraped Metadata")


def step_2():
    logging.info("Scraped Main Data")


def step_3():
    logging.info("Cleaned Main Data")


def step_4():
    logging.info("Geocoded Cleaned Data")


def step_5():
    logging.info("Standardized Geocoded Data")


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
