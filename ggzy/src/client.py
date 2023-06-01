# import dotenv
import logging

from datetime import datetime

from dependencies.scraping.scraper import Scraper
from dependencies.cleaning.cleaning import Cleaner


# dotenv.load_dotenv(".env")
logging.basicConfig(level=logging.INFO)

url = "http://deal.ggzy.gov.cn/ds/deal/dealList_find.jsp"

# In each step create an object of the class, initialize the class with 
# required configuration and call the run method 
def step_1():
    scraper = Scraper(url)
    scraper.run()
    logging.info("Scraped Metadata")


def step_2():
    cleaner = Cleaner()
    cleaner.run()
    logging.info("Cleaned Main Data")



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
