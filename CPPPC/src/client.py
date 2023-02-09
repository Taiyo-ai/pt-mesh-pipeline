import dotenv
import logging

from datetime import datetime

# Importing scraping and data processing modules
from dependencies.scraping.scraper import Scrap
from dependencies.cleaning.cleaning import clean
# from dependencies.geocoding.<file_name> import <class_name>
from dependencies.standardization.standardizer import standardizer

dotenv.load_dotenv(".env")
logging.basicConfig(level=logging.INFO)


# In each step create an object of the class, initialize the class with 
# required configuration and call the run method 
def step_1():
    Scrap_Obj = Scrap(url)
    global r
    r = Scrap_Obj.run()
    logging.info("Data Sccessfully Scraped!")

def step_2():
    Clean_Obj = clean(r)
    global s
    s = Clean_Obj.run()
    logging.info("Data Successfully Cleaned!")


def step_3():
    Standardize_Obj = standardizer(s)
    Doc = Standardize_Obj.run()
    logging.info("Data Successfully Standardized!")
    return Doc


def step_4():
    logging.info("Geocoded Cleaned Data")


if __name__ == "__main__":
    
    # Initializing url as Global Variable
    global url

    # Assingning string value to url
    url = "https://www.cpppc.org/en/PPPyd.jhtml"

    # Running steps sequentially
    step_1()
    step_2()
    step_3()
    step_4()

    print("The Required Data" , step_3())

    logging.info(
        {
            "last_executed": str(datetime.now()),
            "status": "Pipeline executed successfully",
        }
    )
