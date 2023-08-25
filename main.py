# Import packages
from bs4 import BeautifulSoup
import requests
import pandas as pd

# creating a nested dictionary with Tender Title, Reference No, Bid Opening Date, Bid Closing Date as key
bid_data = {"Tender Title": [],
            "Reference No": [],
            "Bid Opening Date": [],
            "Bid Closing Date": []}

# target link
link = requests.get("https://etenders.gov.in/eprocure/app")
webpage = link.text


# Scrapping required data from target link
soup = BeautifulSoup(webpage, 'html.parser')

# Looping through id's using string concatenation to scrape data
tender_list = []
for num in range(0, 9):
    tender_data = soup.find(id="informal_" + str(num)).find_all("td")
    tender_list.append(tender_data)


# Looping through the scraped data to add the cleaned data to the dictionary
for i in tender_list:
    bid_data["Tender Title"].append(i[0].get_text().split(".")[1])
    bid_data["Reference No"].append(i[1].get_text())
    bid_data["Bid Opening Date"].append(i[2].get_text())
    bid_data["Bid Closing Date"].append(i[3].get_text())


# Creating pandas data frame using dictionary
df = pd.DataFrame(bid_data)

# Creates csv file using the data frame
df.to_csv("Tender Data")