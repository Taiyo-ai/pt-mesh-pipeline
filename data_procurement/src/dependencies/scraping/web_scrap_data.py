import requests
from bs4 import BeautifulSoup 
import re
import pandas as pd

class scrapper():
    def __init__(self,url) -> None:
        self.url = url
    
    def fetch_data(self):
        response = requests.get(self.url)
        if response.status_code==200:
            page_contents = response.text
        else:
            #log error
            print("error -- "+response.status_code)
        return page_contents
    
    def format_data(self,page_contents):
        doc = BeautifulSoup(page_contents,'lxml')
        body=doc.find_all("tr")
        header=body[0]
        body_rows=body[1:]
        headings=[]
        for item in header.find_all("th"):
            item=(item.text).rstrip("\n")
            headings.append(item)
        all_rows=[]
        for row_num in range(len(body_rows)):
            row=[]
            for row_item in body_rows[row_num].find_all("td"):
                aa=re.sub("(\xa0)|(\n)|,","",row_item.text)
                row.append(aa)
            all_rows.append(row)
        Event_urls = []
        for row_num in range(len(body_rows)):
            for row_item in body_rows[row_num].find_all('a',href=True):
                aa=row_item['href']
            Event_urls.append(aa)
        df=pd.DataFrame(data=all_rows,columns=headings)
        df.insert(3,"Event_urls",Event_urls,True)
        return df