import re
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from bs4 import BeautifulSoup

def save_page(fname, text):
    with open(fname, "w") as f:
        f.write(text)

def read_page(fname):
    with open(fname, "r") as f:
        contents = f.read()
    return contents


class ScraperTendersIndia:
    def __init__(self, **kwargs):
        self.config = kwargs.get("config")

        options = Options()
        userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
        options.add_argument(f'user-agent={userAgent}')
        options.add_argument('--headless')
        options.add_argument('--log-level=1')
        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.organisation_tender_urls = []

        self.meta_data = []

        self.data = []
        self.data_dir = "../../../../data"

    def load_data(self):
        """Function to load data"""
        self.intial_scrape_url = "https://etenders.gov.in/eprocure/app?page=FrontEndTendersByOrganisation&service=page"

    def do_something(self):
        """Do extraction or processing of data here"""
        self.driver.get(self.intial_scrape_url)

        contents = self.driver.page_source
        soup = BeautifulSoup(contents, features="html.parser")
        data = []
        table = soup.find('table', attrs={'id':'table'})
        table_body = table.find('tbody')

        rows = table_body.find_all('tr')

        base_url = "https://etenders.gov.in"

        
        ## 1st and last rows ignored (dont contain actual data)
        for i in range(1, len(rows)-1):
            row = rows[i]
            cols = row.find_all('td')
            #print(cols)

            meta_data_row = [re.sub(r'\s+', '', e.text) for e in cols[1:] ]
            #print(meta_data_row)

            self.meta_data.append(meta_data_row)

            curr_url =  base_url + cols[2].a["href"]
            self.organisation_tender_urls.append(curr_url)

        self.extract_all_organisations()


    def extract_all_organisations(self):
        for url in self.organisation_tender_urls:
            self.driver.get(url)
            contents = self.driver.page_source
            res = self.extract_single_organsiation(contents)
   


    def extract_single_organsiation(self, contents):
        soup = BeautifulSoup(contents, "html.parser")
        table = soup.find('table', attrs={'id':'table'})
        table_body = table.find('tbody')

        rows = table_body.find_all('tr')
        for i in range(1, len(rows) - 1):
            row = rows[i]
            cols = row.find_all('td')

            base_url = "https://etenders.gov.in"
            tender_url = base_url + cols[4].a["href"]

            self.driver.get(tender_url)
            
            tender_contents = self.driver.page_source
            tender_value_inr, pincode = self.extract_tender_details(tender_contents)

            cols = [re.sub(r'\s+', '', e.text) for e in cols ]

            self.data.append(cols[1:] + [tender_value_inr, pincode])

    def extract_tender_details(self, contents):
        soup = BeautifulSoup(contents, features="html.parser")

        ## tender value
        td_tender_val1 = soup.find('td', string=re.compile(r"Tender\sValue"));
        td_tender_val2 = td_tender_val1.findNext('td')
        tender_value_inr = td_tender_val2.text.strip().replace(",", "")

        ### pin code
        td_pincode1 = soup.find('td', string=re.compile(r"Pincode"));
        td_pincode2 = td_pincode1.findNext('td')
        pincode = td_pincode2.text.strip()

        return tender_value_inr, pincode

    def save_data(self):
        """Function to save data"""

        ## save meta data
        metadata_col_names = ["Organisation Name", "Tender Count"]
        metadata_df = pd.DataFrame(self.meta_data, columns=metadata_col_names)
        #print(metadata_df)

        metadata_df.to_csv(self.config["path_config"]["meta_data_path"], index=False)


        ## save main data
        col_names = ["e-Published Date", "Closing Date", "Opening Date", "Title and Ref.No./Tender ID", "Organisation Chain", "tender_value_inr", "pincode"]
        df = pd.DataFrame(self.data, columns=col_names)
        #print(df)

        df.to_csv(self.config["path_config"]["raw_data_path"], index=False)

        return None

    def run(self):
        """Load data, do_something and finally save the data"""

        self.load_data()

        self.do_something()

        self.save_data()

        return None


    def __del__(self):
        self.driver.close()
        self.driver.quit()

    
if __name__ == "__main__":
    config = {
        # path configurations
        "path_config": {
            "meta_data_path": "../../../../data/meta_data.csv",
            "raw_data_path": "../../../../data/raw_data.csv",
            "cleaned_data_path": "../../../../data/cleaned_data.csv",
            "geocoded_data_path": "../../../../data/geocoded_data.csv",
            "standardized_data_path": "../../../../data/standardized_data.csv",
        }
    }
    obj = ScraperTendersIndia(config = config)
    obj.run()
