import dotenv
import logging

from datetime import datetime

# Importing scraping and data processing modules
from dependencies.scraping.scraper import Scraper
#from dependencies.scraping.<file_name> import <class_name>
from dependencies.cleaning.cleaning import DataCleaner
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
    object = Scraper('https://etenders.gov.in/eprocure/app')
    object.save_to_csv("../../data/raw_data.csv")
    object.run()

def step_3():
    logging.info("Cleaned Main Data")


def step_4():
    logging.info("Geocoded Cleaned Data")
    df = pd.read_csv("../../data/raw_data.csv")
    cleaner = DataCleaner(df)
    cleaned_df = cleaner.clean_data()
    cleaned_df.to_csv("../../data/cleaned_data.csv", index=False)
    cleaner.run()

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
# scraper = Scraper('https://etenders.gov.in/eprocure/app')
# scraper.save_to_csv('raw_data.csv')

# df = pd.read_csv('raw_data.csv')
# cleaner = DataCleaner(df)
# cleaned_df = cleaner.clean_data()
# cleaned_df.to_csv('cleaned_data.csv', index=False)

