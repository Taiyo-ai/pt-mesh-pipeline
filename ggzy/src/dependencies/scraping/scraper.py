import logging
import re
import os
import json
import requests
import pandas as pd

from . import get_page


class Scraper():
    
    def __init__(self, url):
        self.url = url
    
    def run(self):
        logging.info("Scraping started")
        
        payload = "TIMEBEGIN_SHOW=2023-05-23&TIMEEND_SHOW=2023-06-01&TIMEBEGIN=2023-05-23&TIMEEND=2023-06-01&SOURCE_TYPE=1&DEAL_TIME=02&DEAL_CLASSIFY=00&DEAL_STAGE=0001&DEAL_PROVINCE=0&DEAL_CITY=0&DEAL_PLATFORM=0&BID_PLATFORM=0&DEAL_TRADE=0&isShowAll=1&PAGENUMBER=1&FINDTXT="
        
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'JSESSIONID=74592f4161d27a44465375aca4d2; insert_cookie=96816998',
            'Origin': 'http://deal.ggzy.gov.cn',
            'Referer': 'http://deal.ggzy.gov.cn/ds/deal/dealList.jsp',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36 Edg/113.0.1774.57',
            'X-Requested-With': 'XMLHttpRequest'
        }
        
        response = requests.request("POST", self.url, headers=headers, data=payload)
        response = response.json()

        data = response["data"]
        df = pd.DataFrame(data)
        
        os.chdir("../../")
        folder_path = os.getcwd()
        file_path = os.path.join(folder_path + "\data", "raw_data.csv")

        
        df.to_csv(file_path, index=False)
        
    

            
        
        
    
    