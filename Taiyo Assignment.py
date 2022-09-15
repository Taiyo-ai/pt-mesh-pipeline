#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import pandas as pd
from bs4 import BeautifulSoup

class Person:
    def init(self,a ):
        self.a = a

    def abc(b):
        
        csv_file = []
        base_url = b.a
        for page in range(1, 125):
            r = requests.get(base_url + str(page) + "#dashboard_notices.html")
            c = r.content
            soup = BeautifulSoup(c, 'html.parser')
            all_data = soup.find_all("div", {"class": "search-result"})
            #print(all_data)
            for item in all_data:  
                d = {}

                d["Tender"] = item.find("a", {"class": ["govuk-link", "search-result-rwh", "break-word"]}).text

                d["Company"] = item.find("div", {"class": ["search-result-sub-header", "wrap-test"]}).text

                d["Procurement"] = item.find_all("div", {"class": "search-result-entry"})[0].text.replace("Procurement stage", " ")

                d["Notice"] = item.find_all("div", {"class": "search-result-entry"})[1].text.replace("Notice status"," ")

                d["Location"] = item.find_all("div", {"class": "search-result-entry"})[3].text.replace("Contract location", " ")


                try:

                    d["Closing"] = item.find_all("div", {"class": "search-result-entry"})[2].text.replace("Closing"," ")

                except:

                    d["Closing"] = "None"
                try:
                    d["Value"] = item.find_all("div", {"class": "search-result-entry"})[4].text.replace("Contract value", " ")
                except:
                    d["Value"] = "None"
                try:
                    d["Date"] = item.find_all("div", {"class": "search-result-entry"})[5].text.replace("Publication date", " ")
                except:
                    d["Date"] = "None"
                csv_file.append(d)

        df=pd.DataFrame(csv_file)
        df.to_csv("Scraper.csv",index=False)


# In[ ]:


p1 = Person("https://www.contractsfinder.service.gov.uk/Search/Results?&page=")
p1.abc()

