import os
import logging
import boto3

from datetime import datetime

from dependencies.scraping.IIGMetadataScraper import IIGMetadataScraper  # type: ignore
from dependencies.scraping.IIG import IIGScraper  # type: ignore
from dependencies.cleaning.IIG import clean_IIG  # type: ignore
from dependencies.geocoding.IIG import extract_geocode_IIG  # type: ignore
from dependencies.standardisation.IIG import IIGStandardiser  # type: ignore
from dependencies.es_ingestion.IIG_ingestion import IIGIngestion
from dependencies.utils import load_config_yaml  # type: ignore

logging.basicConfig(level=logging.INFO)


def step_1():
    path_config = load_config_yaml()["paths"]["IIG"]
    config = {
        "options": [
            "--headless",
            "--start-fullscreen",
            "--no-sandbox",
            "--allow-insecure-localhost",
        ],
        "master_data_path": path_config["master_data_path"],
        "successful_urls_path": path_config["successful_urls_path"],
        "failed_urls_path": path_config["failed_urls_path"],
        "reference_urls_path": path_config["reference_urls_path"],
        "base_data_path": path_config["base_data_path"],
    }
    IIGMetadataScraper(config=config).run()
    logging.info("Scraped Metadata")


def step_2():
    path_config = load_config_yaml()["paths"]["IIG"]
    config = {
        "executable_path": "src/ppp_scrapers/scrapers/chromedriver/chromedriver.exe",
        "options": [
            "--headless",
            "--start-fullscreen",
            "--no-sandbox",
            "--allow-insecure-localhost",
        ],
        "iig_urls_path": path_config["reference_urls_path"],
        "iig_success_urls_path": path_config["successful_urls_path"],
        "iig_failed_urls_path": path_config["failed_urls_path"],
        "iig_data_path": path_config["master_data_path"],
    }

    scraper = IIGScraper(config)
    scraper.run()
    logging.info("Scraped Main Data")


def step_3():
    clean_IIG().run()
    logging.info("Cleaned Main Data")


def step_4():
    path_config = load_config_yaml()["paths"]["IIG"]
    config = {"path_config": path_config}
    geomapper = extract_geocode_IIG(config=config)
    geomapper.run()
    logging.info("Geocoded Cleaned Data")


def step_5():
    path_config = load_config_yaml()["paths"]["IIG"]
    config = {
        "columns": [
            "sector",
            "sub_sector",
            "project_name",
        ],
        "geocoded_data_path": path_config["geocoded_data_path"],
        "standardized_data_path": path_config["standardized_data_path"],
        "metadata_path": path_config["metadata_path"],
    }
    standardizer = IIGStandardiser(config=config)
    standardizer.run()
    logging.info("Standardising Cleaned Data")


def step_6():
    config = load_config_yaml()["paths"]["IIG"]
    IIGIngestion(config=config).run()


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
