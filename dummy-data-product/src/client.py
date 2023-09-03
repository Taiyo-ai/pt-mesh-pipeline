import dotenv
import logging
from datetime import datetime

# Importing scraping and data processing modules
from dependencies.scraping.scraper import extract_metadata
from dependencies.scraping.scraper import extract_raw_data
from dependencies.cleaning.cleaning import step_3
from dependencies.geocoding.geocoder import step_4
from dependencies.standardization.standardizer import step_5

dotenv.load_dotenv(".env")
logging.basicConfig(level=logging.INFO)

# Define a dictionary to map step names to their corresponding functions
step_functions = {
    "step_1": extract_metadata,
    "step_2": extract_raw_data,
    "step_3": step_3,
    "step_4": step_4,
    "step_5": step_5,
}

def step_1():
    logging.info("Step 1: Scraping Metadata")
    scraper = extract_metadata(config)
    scraper.run()

def step_2():
    logging.info("Step 2: Scraped Main Data")
    main_data_scraper = extract_raw_data(config)
    main_data_scraper.run()

def step_3():
    logging.info("Step 3: Cleaned Main Data")
    cleaner = step_3(config)
    cleaner.run()

def step_4():
    logging.info("Step 4: Geocoded Cleaned Data")
    geocoder = step_4(config)
    geocoder.run()

def step_5():
    logging.info("Step 5: Standardized Geocoded Data")
    standardizer = step_5(config)
    standardizer.run()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--step", help="Step to be chosen for execution")

    args = parser.parse_args()

    config = {}  # Define your configuration here

    selected_step = step_functions.get(f"step_{args.step}")

    if selected_step:
        selected_step()
        logging.info(
            {
                "last_executed": str(datetime.now()),
                "status": "Pipeline executed successfully",
            }
        )
    else:
        logging.error(f"Step '{args.step}' not found.")
