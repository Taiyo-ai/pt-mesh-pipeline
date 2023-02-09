# requests is imported to send get request to the server
# logging is import to keep record of the activities going on

# pandas is imported to convert the parsed data into rows and columns (2D Array)

import requests
import logging

class Scrap:

    # Creating Constructor
    def __init__(self, URL):
        self.URL = URL

    # Creating a Method to Scrap Data
    def Scrap_(self):
        # Sending get request
        response = requests.get(self.URL)
        return response

    # Running Process
    def run(self):
        # Scraping Started
        logging.info("Scraping Started")

        # returned response
        r = self.Scrap_()

        # Straping Completed
        logging.info("Scraping Completed")
        
        return r


if __name__ == "__main__":
    pass