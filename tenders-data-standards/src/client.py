import dotenv
import logging
import os
from datetime import datetime

# Importing scraping and data processing modules
from dependencies.scraping.scraper import Scarper
from dependencies.cleaning.cleaning import CleanigData
from dependencies.geocoding.geocoder import Geocode
from dependencies.standardization.standardizer import Stadardization

dotenv.load_dotenv(".env")
logging.basicConfig(level=logging.INFO)


# In each step create an object of the class, initialize the class with
# required configuration and call the run method
def step_1():
    logging.info("Scraped Metadata")
    webdriver_path = os.environ.get("WEBDRIVER_PATH")
    processes = int(os.environ.get("PROCESSES", 15))
    config = {
        # class specific configuration
        "webdriver_path": webdriver_path,
        "PROCESSES": processes,

    }

    obj = Scarper(config=config)
    obj.run()


def step_2():
    logging.info("Cleaned Main Data")
    csvfile = os.environ.get("CSV_FILE")
    obj = CleanigData(csvfile=csvfile)
    obj.run()

def step_3():
    logging.info("Geocoded Cleaned Data")
    csvfile = os.environ.get("CSV_FILE")
    obj = Geocode(csvfile=csvfile)
    obj.run()

def step_4():
    logging.info("Standardized Geocoded Data")
    csvfile = os.environ.get("CSV_FILE")
    obj = Stadardization(csvfile=csvfile)
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
