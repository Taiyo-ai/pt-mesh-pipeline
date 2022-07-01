from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pandas as pd

class Scraper:
    """
    Scrapper Class for scrapping 'Contracts Out for Bid' data from California Procurement
    """
    def __init__(self):
        self.session = HTMLSession()
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
        self.url = 'https://dot.ca.gov/programs/procurement-and-contracts/contracts-out-for-bid'

    def extract(self):
        """
        Function to scrap and clean the data and write the cleaned data into a csv file  
        """
        r = self.session.get(self.url, headers=self.headers)
        
        soup = BeautifulSoup(r.content, 'html5lib')

        table = soup.find('table', {'class':'table'}) # table 

        table_head = table.find('thead') # table head 
        table_body = table.find('tbody') # table body

        headers = table_head.find_all('tr')
        rows = table_body.find_all('tr')

        data = [] 

        for header in headers:
            cols = header.find_all('th')
            cols = [ele.text.strip() for ele in cols]
            link = ['Event Details Link'] # Extra column to add Event Details link
            data.append(cols + link) 

        for row in rows:
            cols = row.find_all('td')
            try:
                link = []
                for i in cols:
                    link.append(i.a['href']) # getting the event link
            except:  
                pass # only one 'td' has href link and other two 'td' has only text
                     # handling the error using try except block
    
            cols = [ele.text.strip() for ele in cols] 
            data.append([ele for ele in cols if ele] + link) # getting rid of empty values
            

        df = pd.DataFrame(data) # conerting the list into DataFrame
        df.to_csv('data/Contracts_out_for_bid.csv', index=False, header=False) 
        print("Data has been scraped and saved in .csv format in 'data' folder")
        return df

if __name__ == '__main__':
    scraping = Scraper()
    data = scraping.extract()
    print(data)