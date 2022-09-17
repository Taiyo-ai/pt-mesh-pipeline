import os
import dotenv
import logging

from datetime import datetime
from chromedriver_py import binary_path

from dependencies.scraping.eProcIndCanCentral import EPICancelledCentralScraper
from dependencies.cleaning.EPI import clean_EPI
from dependencies.geocoding.epi import EPIGeocoder
from dependencies.standardization.epi import EPIStandardiser
from dependencies.utils import load_config_yaml
from dependencies.es_ingestion.epi_ingestion import EPIIngestion

dotenv.load_dotenv(".env")
logging.basicConfig(level=logging.INFO)


# Year 2016
def step_1():
    path_config = load_config_yaml()["paths"]["EPICANC"]
    config = {
        "executable_path": binary_path,
        "options": [
            "--headless",
            "--no-sandbox",
            "--start-fullscreen",
            "--allow-insecure-localhost",
            "--disable-dev-shm-usage",
        ],
        "drop_duplicates": ["tender_reference_number"],
        "year": "2016",
        "epictc_master_data_path": path_config["master_data_path"],
    }

    scraper = EPICancelledCentralScraper(config=config)
    scraper.run()
    logging.info("Scraped Raw data")


def step_2():
    extra_config = {"source_abbr": "EPICANC", "year": "2016"}
    clean_EPI(extra_config=extra_config).run()
    logging.info("Cleaned Main Data")


def step_3():
    APIKEY = os.getenv("POSITION_STACK_API_KEY")
    path_config = load_config_yaml()["paths"]["EPICANC"]

    for key in list(path_config.keys()):
        path_config[key] = path_config[key].replace("<year>", "2016")

    geomapper = EPIGeocoder(config=path_config, api_key=APIKEY)
    geomapper.run()
    logging.info("Geocoded Cleaned Data")


def step_4():
    path_config = load_config_yaml()["paths"]["EPICANC"]

    for key in list(path_config.keys()):
        path_config[key] = path_config[key].replace("<year>", "2016")

    config = {
        "columns": [
            "product_category",
            "product_sub_category",
            "tender_category",
            "title",
        ],
        "geocoded_data_path": path_config["geocoded_data_path"],
        "standardised_data_path": path_config["standardized_data_path"],
        "metadata_path": path_config["metadata_path"],
    }
    standardizer = EPIStandardiser(config=config)
    standardizer.run()
    logging.info("Standardising Cleaned Data")


def step_5():
    path_config = load_config_yaml()["paths"]["EPIHVTC"]
    EPIIngestion(config=path_config).run()
    logging.info("Ingestion Data Done")



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
