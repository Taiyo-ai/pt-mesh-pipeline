import dotenv
import logging
from dependencies.scraping.scraper import Scraper
from dependencies.cleaning.cleaning import Cleaner
from dependencies.standardization.standardizer import Standard

from datetime import datetime
import pandas as pd

# Importing scraping and data processing modules
# from dependencies.scraping.<file_name> import <class_name>
# from dependencies.scraping.<file_name> import <class_name>
# from dependencies.cleaning.<file_name> import <class_name>
# from dependencies.geocoding.<file_name> import <class_name>
# from dependencies.standardization.<file_name> import <class_name>

dotenv.load_dotenv(".env")
logging.basicConfig(level=logging.INFO)


# In each step create an object of the class, initialize the class with 
# required configuration and call the run method 
def step_1():
    logging.info("Scraped Metadata")


def step_2():
    logging.info("Scraped Main Data")
    url = "https://etenders.gov.in/eprocure/app"
    scraper = Scraper(url)
    scraped_data = scraper.scraping_data()

    #Column title of the data
    columns = ["S.No", "e-Published Date", "Bid Submission Closing Date", "Tender Opening Date", "Title and Ref", "Organisation Chain"]
    df = pd.DataFrame(scraped_data, columns=columns)

    #Save the scraped data to a csv file
    df.to_csv("../../data/scraped_data.csv", index=False)


def step_3():
    logging.info("Cleaned Main Data")
    # Read the scraped data from csv file
    data = "../../data/scraped_data.csv"
    cleaner = Cleaner(data)
    cleaned_data = cleaner.arrange_title_column()

    #Remove duplicate rows
    cleaned_data = cleaner.remove_duplicate_rows()

    #Remove rows with missing data
    cleaned_data = cleaner.remove_rows_with_empty_values()

    #Store cleaned data to a csv file
    cleaned_data.to_csv("../../data/cleaned_data.csv", index=False)


def step_4():
    logging.info("Geocoded Cleaned Data")


def step_5():
    logging.info("Standardized Geocoded Data")
    data = "../../data/cleaned_data.csv"
    standard = Standard(data)

    #Convert date into datetime standard
    standard_data = standard.datetime_convert()

    #Rename columns as per lower snake casing standard
    standard_data = standard.rename_columns()

    #Store to standard cleaned data in csv format
    standard_data.to_csv("../../data/standard_cleaned_data.csv", index=False)

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
