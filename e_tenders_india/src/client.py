import os
import dotenv
import logging

from datetime import datetime

from dependencies.utils import load_config_yaml  # type: ignore
from dependencies.scraping.eTendersIndiaMetadataScraper import eTendersIndiaMetadataScraper  # type: ignore
from dependencies.cleaning.eTendersIndia import clean_eTendersIndia  # type: ignore
from dependencies.geocoding.etendersindia_geocode import eTendersIndiaGeocoder  # type: ignore
from dependencies.standardisation.eTendersIndiaStandardiser import eTendersIndiaStandardiser  # type: ignore
from dependencies.es_ingestion.etenders_ingestion import eTendersIndiaIngestion

dotenv.load_dotenv(".env")
logging.basicConfig(level=logging.INFO)


def step_1():
    path_config = load_config_yaml()["paths"]["ETENDERSINDIA"]
    eTendersIndiaMetadataScraper(config=path_config).run()
    logging.info("Scraped Metadata and Data")


def step_2():
    clean_eTendersIndia().run()
    logging.info("Cleaned Main Data")


def step_3():
    path_config = load_config_yaml()["paths"]["ETENDERSINDIA"]
    APIKEY = os.getenv("POSITION_STACK_API_KEY")
    eTendersIndiaGeocoder(config=path_config, api_key=APIKEY).run()
    logging.info("Geocoded Cleaned Data")


def step_4():
    path_config = load_config_yaml()["paths"]["ETENDERSINDIA"]
    path_config["columns"] = ["tender_category", "sub_category", "product_category"]
    eTendersIndiaStandardiser(config=path_config).run()
    logging.info("Standardised Cleaned Data")


def step_5():
    path_config = load_config_yaml()["paths"]["ETENDERSINDIA"]
    eTendersIndiaIngestion(config=path_config).run()
    logging.info("Ingested into ElasticSearch")

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
