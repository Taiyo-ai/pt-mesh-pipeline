import dotenv
from dependencies.utils.logging import logger
import os
from datetime import datetime

# Importing scraping and data processing modules

from dependencies.scraping.scraper import WebScrapper
from dependencies.cleaning.cleaning import CleanData
from dependencies.geocoding import geocoder
from dependencies.standardization.standardizer import Standardizer

dotenv.load_dotenv(".env")


# In each step create an object of the class, initialize the class with
# required configuration and call the run method

def step_1():
    logger.info("Scraped Main Data")

    URL = os.getenv("URL")  # setting url

    web_scrapper = WebScrapper(URL)  # creating WebScrapper class object
    web_scrapper.run()


def step_2():
    logger.info("Cleaned Main Data")
    CleanData.run()


def step_3():
    logger.info("Geocoded Cleaned Data")
    geocoder.run()


def step_4():
    logger.info("Standardized Geocoded Data")
    Standardizer.run()


def step_():
    logger.info("No argument provided , Running all methods")
    step_1()
    step_2()
    step_3()
    step_4()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--step", help="step to be choosen for execution")

    args = parser.parse_args()

    print("args  ", args)
    print(f"step_{args.step}()")

    eval(f"step_{args.step}()")

    logger.info(
        {
            "last_executed": str(datetime.now()),
            "status": "Pipeline executed successfully",
        }
    )
