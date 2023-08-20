import dotenv
import json
import logging

from datetime import datetime
from dataclasses import asdict

from dependencies.scraping.scraper import DataScraper
from dependencies.scraping.models import TendersMetaData
from dependencies.scraping.utils import list_raw_tenders, fetch_tender
from dependencies.utils.store import Store

dotenv.load_dotenv(".env")
logging.basicConfig(level=logging.INFO)


# In each step create an object of the class, initialize the class with
# required configuration and call the run method
def step_1():
    scraper = DataScraper("https://etenders.gov.in/eprocure/app")
    soup = scraper.scrape()

    store = Store("../../data/metadata.jsonl")
    for raw_tender in list_raw_tenders(soup):
        store.save(asdict(raw_tender))

    logging.info("Scraped Metadata")


def step_2():
    metadata_store = Store("../../data/metadata.jsonl")
    scrapeddata_store = Store("../../data/scrapeddata.jsonl")
    for tender_meta in metadata_store.read():
        meta = json.loads(tender_meta)
        tender = fetch_tender(TendersMetaData(**meta))
        scrapeddata_store.save(tender)

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
