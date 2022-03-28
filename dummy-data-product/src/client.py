# import dotenv
import logging

from datetime import datetime

# Importing scraping and data processing modules
from dependencies.scraping.scraper import Scraper
# from dependencies.scraping.<file_name> import <class_name>
# from dependencies.cleaning.<file_name> import <class_name>
# from dependencies.geocoding.<file_name> import <class_name>
# from dependencies.standardization.<file_name> import <class_name>

# dotenv.load_dotenv(".env")
logging.basicConfig(level=logging.INFO)


# In each step create an object of the class, initialize the class with 
# required configuration and call the run method 
def step_1():
    """ This method will scrape the data from the website """
    obj = Scraper()
    obj.getMetadata()
    logging.info("Scraped Metadata")

def step_2():
    obj = Scraper()
    obj.getScrapedData()
    logging.info("Scraped Main Data")
    # return 

def step_3():
    obj = Scraper()
    scraped_data = obj.getScrapedData()
    obj.doCleanup(scraped_data)
    logging.info("Cleaned Main Data")


def step_4():
    obj = Scraper()
    scraped_data = obj.getScrapedData()
    features= obj.doCleanup(scraped_data)
    obj.generateCSV(features)
    logging.info("Generated CSV")


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
