import dotenv
import logging

from datetime import datetime

# Importing scraping and data processing modules
from src.dependencies.scraping.scraper import TenderScraper
from src.dependencies.cleaning.cleaner import *
from src.dependencies.geocoding.geocoder import LocationExtractor
from src.dependencies.standardization.standardizer import SectorExtractor

dotenv.load_dotenv(".env")
logging.basicConfig(level=logging.INFO)

import csv
import os
import pandas as pd
import re
# In each step create an object of the class, initialize the class with 
# required configuration and call the run method 
def step_1():
    logging.info("Scraped Metadata")


def step_2():
    geckodriver_path = os.getenv("geckodriver_path") 
    url = os.getenv("url") 

    scraper = TenderScraper(geckodriver_path, url)
    scraper.start()
    tender_data = scraper.scrape_tenders()

    # Specify the CSV file path
    csv_file_path = os.getenv("csv_file_path")

    # Save the data to a CSV file
    with open(csv_file_path, mode='w', newline='') as csv_file:
        fieldnames = ["S.No", "e-Published Date", "Bid Submission Closing Date", "Tender Opening Date", "Title and Ref.No./Tender ID", "Details"]
        writer = csv.writer(csv_file)
        writer.writerow(fieldnames)
        for tender in tender_data:
            writer.writerow(tender)

    print(f"Data saved to {csv_file_path}")

    logging.info("Scraped Main Data")


def step_3():
    logging.info("Cleaned Main Data")


def step_4():
    # Example usage
    extractor = LocationExtractor()

    try:
        # Read CSV file into a pandas DataFrame
        df = pd.read_csv(os.getenv("csv_file_path"))

        # Initialize an empty list to store locations
        locations_list = []

        # Iterate over rows and process the "details" column
        for _, row in df.iterrows():
            details = row['Details']
            locations = extractor.process_and_extract(details)
            
            # Check if locations were found, and if not, add "NA"
            if not locations:
                locations = "NA"
            
            locations_list.append(locations)

        # Add the extracted locations as a new column "locations"
        df['Locations'] = locations_list

        # Save the modified DataFrame back to the CSV file
        df.to_csv(os.getenv("csv_file_path"), index=False)

        logging.info("Geocoded Cleaned Data")
    
    except Exception as e:
        logging.info(e)


def step_5():
    try:
        # Example usage
        extractor = SectorExtractor()

        # Read CSV file into a pandas DataFrame
        df = pd.read_csv(os.getenv("csv_file_path"))

        # Initialize lists to store sector and subsector
        sector_list = []
        subsector_list = []

        # Iterate over rows and process the "Title and Ref.No./Tender ID" column
        for index, row in df.iterrows():
            title_ref = row['Title and Ref.No./Tender ID']
            # Extract the first bracket value from the title_ref
            match = re.search(r'\[(.*?)\]', title_ref)
            if match:
                title_ref = match.group(1)
            else:
                title_ref = ""

            sector, subsector = extractor.extract_sector_subsector(title_ref)
            
            # Check if sector and subsector were extracted, otherwise use "NA"
            sector_list.append(sector if sector else "NA")
            subsector_list.append(subsector if subsector else "NA")

        # Add the extracted or "NA" sector and subsector to the DataFrame
        df['Sector'] = sector_list
        df['Subsector'] = subsector_list

        # Save the modified DataFrame back to the CSV file
        df.to_csv(os.getenv("csv_file_path"), index=False)

        logging.info("Standardized Geocoded Data")

    except Exception as e:
        logging.info(e)    


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
