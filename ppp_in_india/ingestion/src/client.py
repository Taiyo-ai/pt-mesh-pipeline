import os
import dotenv
import logging

from datetime import datetime

from dependencies.utils import load_config_yaml
from dependencies.scraping.PPP_INDIA_METASCRAPER import PPPINDIAMetadataScraper
from dependencies.scraping.PPPINDIASCRAPER import PPPINDIAScraper
from dependencies.cleaning.pppIndia_clean import clean_PPPIndia

dotenv.load_dotenv(".env")
logging.basicConfig(level=logging.INFO)


def step_1():
    path_config = load_config_yaml()["paths"]["PPPINDIA"]
    PPPINDIAMetadataScraper(config=path_config).run()
    logging.info("Scraped Metadata")


def step_2():
    path_config = load_config_yaml()["paths"]["PPPINDIA"]
    PPPINDIAScraper(config=path_config).run()
    logging.info("Scraped Main Data")


def step_3():
    clean_PPPIndia.run()
    logging.info("Cleaned Main Data")


def step_4():
    path_config = load_config_yaml()["paths"]["PPPINDIA"]
    APIKEY = os.getenv("API_KEY")
    logging.info("Geocoded Cleaned Data")


def step_5():
    path_config = load_config_yaml()["paths"]["PPPINDIA"]
    config = {
        "columns": ["sector", "subsector", "segment", "technology"],
        "geocoded_data_path": path_config["geocoded_data_path"],
        "standardised_data_path": path_config["standardised_data_path"],
        "metadata_path": path_config["metadata_path"],
    }
    logging.info("Standardising Cleaned Data")


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
