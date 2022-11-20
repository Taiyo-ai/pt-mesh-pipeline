import dotenv
import logging
import geocoding
import cleaning
import standardizer
from datetime import datetime

# Importing scraping and data processing modules
# from dependencies.scraping.<file_name> import <class_name>
# from dependencies.scraping.<file_name> import <class_name>
# from dependencies.cleaning.<file_name> import <class_name>
# from dependencies.geocoding.<file_name> import <class_name>
# from dependencies.standardization.<file_name> import <class_name>

dotenv.load_dotenv(".env")
logging.basicConfig(level=logging.INFO)


# In each step create an object of the class, initialize the class with 
# required configuration and call the run method 
def step_1():
    logging.info("Scraped Metadata")


def step_2():
    scraper.scrape('EU')
    scraper.scrape('USGOV')
    scraper.scrape('FL')
    scraper.scrape('TX')
    scraper.scrape('CA')
    scraper.scrape('UK')
    logging.info("Scraped Main Data")


def step_3():
    cleaning.functions(args)
    logging.info("Cleaned Main Data")


def step_4():
    geocoding.geocoder(data)
    logging.info("Geocoded Cleaned Data")


def step_5():
    standardize.functions(args)
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
