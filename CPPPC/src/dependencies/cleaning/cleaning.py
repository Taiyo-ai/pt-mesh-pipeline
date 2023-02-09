# logging is import to keep record of the activities going on
# BeautifulSoup is imported to parse the unwanted data and organize and format the data obtained

import logging
from bs4 import BeautifulSoup as bs
import requests

class clean:

    # Creating Constructor
    def __init__(self, r):
        self.r = r
    
    # Creating a Method to Clean Data
    def Clean_(self):
        # Parsing or formatting the obtained data using BeautifulSoup
        res = self.r
        soup = bs(res.content, "html5lib")
        return soup

    # Running Process
    def run(self):
        # Cleaning Started
        logging.info("Cleaning Started")

        # returned formatted Data
        s = self.Clean_()

        # Cleaning Completed
        logging.info("Cleaning Completed")

        return s

if __name__ == "__main__":
    pass