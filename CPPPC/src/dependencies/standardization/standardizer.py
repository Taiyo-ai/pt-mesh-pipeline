# logging is import to keep record of the activities going on
# BeautifulSoup is imported to parse the unwanted data and organize and format the data obtained
# import pandas as pd

import logging
from bs4 import BeautifulSoup as bs
import pandas as pd

class standardizer:

    # Creating Constructor
    def __init__(self, s):
        self.s = s
    
    # Creating a Method to Standardize Data
    def Clean_(self):
        # Creating List to push data
        Data_Record_ = []
    
        # Defining data block which is required
        S = self.s
        Data_Block = S.find("ul", attrs={"class": "new-content ppp-list"})
    
        # Obtaining all such Data_Block Present in the HTML Document
        for row in Data_Block.findAll("li"):
            Data_ = {}
            Data_["Image-Link"] = row.img["src"]
            Data_["Title"] = row.a.text
            Data_["Open-Title"] = row.a["href"]
            Data_["Desc"] = row.div.text
            Data_Record_.append(Data_)
    
        # The Data_Record_ obtained is further being arranged into rows and columns called the DataFrame
        df = pd.DataFrame(Data_Record_, columns=["Image-Link", "Title", "Open-Title", "Desc"])
    
        # The DataFrame is then converted into .csv format
        df.to_csv("data.csv", index=False, sep=" ")

        return pd
    
    # Running Process
    def run(self):
        # Standardizing Started
        logging.info("Cleaning Started")

        # returned .csv file
        p = self.Clean_()

        # Standardization Completed
        logging.info("Cleaning Completed")

        return p

if __name__ == "__main__":
    pass