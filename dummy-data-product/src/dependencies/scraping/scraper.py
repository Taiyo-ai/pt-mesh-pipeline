import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

class ETendersScraper:
    def __init__(self):
         self.url = "https://etenders.gov.in/eprocure/app"
         

        
    def scrape_tender_data(self):
      
        r = requests.get(self.url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            table = soup.find("table", class_="list_table")
            
            titles = []
            reference_numbers = []
            closing_dates = []
            bid_opening_dates = []
 
            for row in table.find_all("tr"):
                cells = row.find_all("td")
                if len(cells) == 4:
                    title = cells[0].text.strip()
                    title = re.sub(r'^\d+\.\s+', '', title)
                    reference_no = cells[1].text.strip()
                    closing_date = cells[2].text.strip()
                    bid_opening_date = cells[3].text.strip()
                    titles.append(title)
                    reference_numbers.append(reference_no)
                    closing_dates.append(closing_date)
                    bid_opening_dates.append(bid_opening_date)
            data = {
                           "Tender Title": titles,
                           "Reference No": reference_numbers,
                           "Closing Date": closing_dates,
                           "Bid Opening Date": bid_opening_dates,
                 }
            df = pd.DataFrame(data)
            df1 = df.iloc[1:]
            return df1

        else:
            print('Failed to fetch data from the website')
            return None