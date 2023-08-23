import dotenv
import logging
from dependencies.scraping.scraper import Scraper

from datetime import datetime
import pandas as pd

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
    url = "https://etenders.gov.in/eprocure/app"
    scraper = Scraper(url)
    scraped_data = scraper.scraping_data()

    #Column title of the data
    columns = ["S.No", "e-Published Date", "Bid Submission Closing Date", "Tender Opening Date", "Title and Ref", "Organisation Chain"]
    df = pd.DataFrame(scraped_data, columns=columns)

    #Save the scraped data to a csv file
    df.to_csv("data/scraped_data.csv")

    scraper.driver_close()


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
