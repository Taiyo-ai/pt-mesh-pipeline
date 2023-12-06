import dotenv
from dotenv import load_dotenv
import logging
from datetime import datetime
from dependencies.scraping.scraper import Scrapper
from dependencies.cleaning.cleaning import clean_data
from dependencies.geocoding.geocoder import geocode_csv
from dependencies.standardization.standardizer import *

def step_1():
    filename = input("Enter csv file name : ")
    writer, file = open_file(filename)
    Scrapper(writer)
    closefile(file)
    logging.info("Scraped Metadata")

def step_2():
    clean_data()
    logging.info("Cleaned Main Data")

def step_3():
    geocode_csv()
    logging.info("Geocoded Cleaned Data")


dotenv.load_dotenv(".env")
logging.basicConfig(level=logging.INFO)

class Main:
    filename = input("Enter csv file name : ")
    writer,file=open_file(filename)
    Scrapper(writer)
    closefile(file)
    t=True
    while(t):
        print("1-->Scrapping Meta Data\n2-->Cleaned Main Data\n3-->Geocoded Cleaned Data")
        stepnum = int(input("Enter step to go :"))
        eval(f"step_{stepnum}()")
        logging.info(
            {
                "last_executed": str(datetime.now()),
                "status": "Pipeline executed successfully",
            })





# In each step create an object of the class, initialize the class with
# required configuration and call the run method

