import dotenv
import logging

from datetime import datetime

from dependencies.scraping.scraper import DataScraper
from dependencies.scraping.utils import list_raw_tenders, fetch_tender
from dependencies.utils.store import Store

dotenv.load_dotenv(".env")
logging.basicConfig(level=logging.INFO)


# In each step create an object of the class, initialize the class with
# required configuration and call the run method
def step_1():
    scraper = DataScraper("https://etenders.gov.in/eprocure/app")
    soup = scraper.scrape()

    store = Store("scrapped_data.jsonl")
    for raw_tender in list_raw_tenders(soup):
        tender_data = fetch_tender(raw_tender)
        store.save(tender_data)

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
