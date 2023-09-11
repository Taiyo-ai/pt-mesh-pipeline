import os
import logging
import boto3

from datetime import datetime

# from chromedriver_py import binary_path

from dependencies.scraping.IIGCSRMetadataScraper import IIGMetadataScraper  # type: ignore
from dependencies.scraping.IIG_CSR import IIGScraper  # type: ignore
from dependencies.cleaning.IIG_CSR import clean_IIG  # type: ignore
from dependencies.geocoding.IIG_CSR import extract_geocode_IIG_CSR  # type: ignore
from dependencies.standardisation.IIG_CSR import IIGCSRStandardiser  # type: ignore
from dependencies.es_ingestion.IIG_CSR import IIGCSRIngestion
from dependencies.utils import load_config_yaml  # type: ignore

logging.basicConfig(level=logging.INFO)


def step_1():
    path_config = load_config_yaml()["paths"]["IIG_CSR"]
    config = {
        "master_data_path": path_config["master_data_path"],
        "successful_urls_path": path_config["successful_urls_path"],
        "failed_urls_path": path_config["failed_urls_path"],
        "reference_urls_path": path_config["reference_urls_path"],
        "base_data_path": path_config["base_data_path"],
    }
    IIGMetadataScraper(config=config).run()
    logging.info("Scraped Metadata")


def step_2():
    path_config = load_config_yaml()["paths"]["IIG_CSR"]
    config = {
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
    geo = extract_geocode_IIG_CSR()
    geo.run()
    logging.info("Geocoded Cleaned Data")


def step_5():
    path_config = load_config_yaml()["paths"]["IIG_CSR"]
    config = {
        "columns": [
            "sector",
            "subsector",
            "description",
            "project_name",
            "funding_details",
        ],
        "geocoded_data_path": path_config["geocoded_data_path"],
        "standardized_data_path": path_config["standardized_data_path"],
        "metadata_path": path_config["metadata_path"],
    }
    standardizer = IIGCSRStandardiser(config=config)
    standardizer.run()
    logging.info("Standardising Cleaned Data")


def step_6():
    config = load_config_yaml()["paths"]["IIG_CSR"]
    IIGCSRIngestion(config=config).run()


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
