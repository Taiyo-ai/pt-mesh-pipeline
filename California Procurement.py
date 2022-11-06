#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Importing Libraries


# In[2]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import seaborn as sns


# In[3]:


#Importing Url
url = "https://dot.ca.gov/programs/procurement-and-contracts/contracts-out-for-bid"    #open link
html = urlopen(url)


# In[4]:


soup = BeautifulSoup(html)


# In[5]:


title = soup.title
print(title)
print(title.text)


# In[6]:


links = soup.find_all('a', href=True)
for link in links:
    print(link['href'])


# In[7]:


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


# In[8]:


df = pd.DataFrame(data)
print(data)


# In[9]:


df = pd.DataFrame(data)
print(df.head())
print(df.tail())


# In[10]:


header_list =[]
col_headers = soup.find_all('th')
for col in col_headers:
    header_list.append(col.text)
print(header_list)


# In[11]:


df.columns = header_list
print(df.head())


# In[12]:


df.info()


# In[13]:


df.shape


# In[14]:


df.describe()


# In[15]:


#Saving output to csv file


# In[16]:


df.to_csv(r'C:/Users/user/Dropbox/PC/Desktop/Machine Learning/Taiyo/web scrapping/Tender.csv', index = False, header = True)


# In[17]:


#reading the saved csv file


# In[18]:


df = pd.read_csv("Tender.csv")


# In[19]:


df.head()


# In[20]:


#renaming of column name for data analysis


# In[21]:


df.rename(columns = {'Event ID':'Event_ID', 'Event Name':'Event_Name', 'End Date':'End_Date'}, inplace = True)


# In[22]:


plt.title('DATE OF EVENTS', fontsize=20)
hist = sns.histplot(df.End_Date)


# In[23]:


d1 = sns.jointplot(data=df, x='Event_ID', y='End_Date')


# In[ ]:




