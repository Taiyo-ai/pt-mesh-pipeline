#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import seaborn as sns


# In[2]:


#Importing Url
url = "https://apps3.txdot.gov/apps-cq/project_tracker/"    #open link
html = urlopen(url)


# In[3]:


soup = BeautifulSoup(html)


# In[4]:


title = soup.title
print(title)
print(title.text)


# In[5]:


links = soup.find_all('a', href=True)
for link in links:
    print(link['href'])


# In[6]:


data = []
allrows = soup.find_all("tr")
for row in allrows:
    row_list = row.find_all("td")
    dataRow = []
    for cell in row_list:
        dataRow.append(cell.text)
    data.append(dataRow)
data = data[1:]
print(data[-2:])


# In[7]:


df = pd.DataFrame(data)
print(data)


# In[8]:


df = pd.DataFrame(data)
print(df.head())
print(df.tail())


# In[9]:


header_list =[]
col_headers = soup.find_all('th')
for col in col_headers:
    header_list.append(col.text)
print(header_list)


# In[10]:


df.info()


# In[11]:


df.shape


# In[12]:


df.describe


# In[13]:


df.to_csv(r'C:/Users/user/Dropbox/PC/Desktop/Machine Learning/Taiyo/web scrapping/Texas.csv', index = False, header = True)


# In[16]:


df = pd.read_csv("Texas.csv")


# In[17]:


df.head()


# In[ ]:





# In[ ]:




