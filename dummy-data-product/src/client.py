import dotenv
import logging
from datetime import datetime
from dependencies.scraping.scraper import scrape_world_bank_data
from dependencies.cleaning.cleaning import clean_data
from dependencies.geocoding.geocoder import geocode_data
from dependencies.standardization.standardizer import standardize_data
import csv
import os

dotenv.load_dotenv(".env")
logging.basicConfig(level=logging.INFO)

# Define the absolute path to the "data" folder
data_folder = os.path.abspath("data")

def save_to_csv(data, filename):
    # Create the data folder if it doesn't exist
    os.makedirs(data_folder, exist_ok=True)

    # Define the full path to the CSV file using the absolute data folder path
    full_path = os.path.join(data_folder, filename)

    # Write data to the CSV file
    with open(full_path, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = data[0].keys() if data else []
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def step_1():
    # Step 1: Scraping Metadata
    logging.info("Scraping Metadata")
    metadata, _ = scrape_world_bank_data()
    # Process metadata if needed
    save_to_csv(metadata, "metadata.csv")  # Save metadata to a CSV file

def step_2():
    # Step 2: Scraping Main Data
    logging.info("Scraping Main Data")
    _, raw_data = scrape_world_bank_data()
    # Process raw_data if needed
    save_to_csv(raw_data, "raw_data.csv")  # Save raw_data to a CSV file

def step_3():
    # Step 3: Cleaning Main Data
    logging.info("Cleaning Main Data")
    _, raw_data = scrape_world_bank_data()  # Fetch raw_data again
    cleaned_data = clean_data(raw_data)
    # Process cleaned_data if needed
    save_to_csv(cleaned_data, "cleaned_data.csv")  # Save cleaned_data to a CSV file

def step_4():
    # Step 4: Geocoding Cleaned Data
    logging.info("Geocoding Cleaned Data")
    _, raw_data = scrape_world_bank_data()  # Fetch raw_data again
    cleaned_data = clean_data(raw_data)  # Clean raw_data again
    geocoded_data = geocode_data(cleaned_data)
    # Process geocoded_data if needed
    save_to_csv(geocoded_data, "geocoded_data.csv")  # Save geocoded_data to a CSV file

def step_5():
    # Step 5: Standardizing Geocoded Data
    logging.info("Standardizing Geocoded Data")
    _, raw_data = scrape_world_bank_data()  # Fetch raw_data again
    cleaned_data = clean_data(raw_data)  # Clean raw_data again
    geocoded_data = geocode_data(cleaned_data)  # Geocode cleaned_data again
    standardized_data = standardize_data(geocoded_data)
    # Process standardized_data if needed
    save_to_csv(standardized_data, "standardized_data.csv")  # Save standardized_data to a CSV file

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--step", help="Step to be chosen for execution")

    args = parser.parse_args()

    if args.step:
        step_function = globals().get(f"step_{args.step}")
        if step_function:
            step_function()
        else:
            logging.error(f"Invalid step: {args.step}") 

    logging.info(
        {
            "last_executed": str(datetime.now()),
            "status": "Pipeline executed successfully",
        }
    )
