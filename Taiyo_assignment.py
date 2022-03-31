#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Importing required Libraries
import selenium
import pandas as pd
import time
from bs4 import BeautifulSoup

# Importing selenium webdriver 
from selenium import webdriver

# Importing required Exceptions which needs to handled
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException

#Importing requests
import requests

# importing regex
import re


# ##### City of Sunnyvale Procurement - Bids & RFPs | DemandStar

# In[24]:


# Activating the chrome browser
driver=webdriver.Chrome("chromedriver.exe") 
time.sleep(3)

# Opening the website
url = "https://www.demandstar.com/app/agencies/california/city-of-sunnyvale/procurement-opportunities/e9a860f4-8f17-43af-aae7-e5dc8389f36e/"
driver.get(url)

time.sleep(2)

#Scroll to the end of the page
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(5)

#Creating empty lists
Name = []
Location = []
ID = []
Due_Date = []
Broadcast_Date = []
Planholders = []
Status = []

#Scraping the names
names = driver.find_elements_by_xpath('//a[@class="mw-75 text-truncate"]')
for n in names:
    Name.append(n.text)
    
#Scraping the location
locations = driver.find_elements_by_xpath('/html/body/div[1]/main/div[2]/div[2]/div/div/div/p')
for l in locations:
    Location.append(l.text)

time.sleep(2)

#Scraping the ID
ids = driver.find_elements_by_xpath('/html/body/div[1]/main/div[2]/div[2]/div/div/div/ul/li[1]')
for i in ids:
    ID.append(i.text)
    
time.sleep(2)

#Scraping the Due date
due = driver.find_elements_by_xpath('/html/body/div[1]/main/div[2]/div[2]/div/div/div/ul/li[2]')
for d in due:
    Due_Date.append(d.text)
    
time.sleep(2)

#Scraping the Broadcast date
broadcasts = driver.find_elements_by_xpath('/html/body/div[1]/main/div[2]/div[2]/div/div/div/ul/li[3]')
for b in broadcasts:
    Broadcast_Date.append(b.text)
    
time.sleep(2)

#Scraping Planholders
plans = driver.find_elements_by_xpath('/html/body/div[1]/main/div[2]/div[2]/div/div/div/ul/li[4]')
for p in plans:
    Planholders.append(p.text)
    
time.sleep(2)

#Scraping Status
status = driver.find_elements_by_xpath('/html/body/div[1]/main/div[2]/div[2]/div/div/div/h5/span')
for s in status:
    Status.append(s.text)
    
time.sleep(2)

#Creating Dataframe to store the results
demandstar_df = pd.DataFrame({'Name': Name,
                             'Location': Location,
                             'ID': ID,
                             'Due Date': Due_Date,
                             'Broadcast Date': Broadcast_Date,
                             'Planholders': Planholders,
                             'Status': Status})

demandstar_df


# In[ ]:




