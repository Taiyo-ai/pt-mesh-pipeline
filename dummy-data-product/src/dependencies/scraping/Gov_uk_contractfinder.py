#!/usr/bin/env python
# coding: utf-8

# In[33]:


from bs4 import BeautifulSoup
import requests

get_ipython().run_line_magic('autosave', '1')


# In[34]:


#fetching the url
url =  f"https://www.contractsfinder.service.gov.uk/Search/Results"

#using .text because we need to convert the output into the text format else it returns 200 means success in the request

source = requests.get(url).text
soup = BeautifulSoup(source,'lxml')

#print with prettify will print the output as a beautiful html file
#      print(soup.prettify())


div_search_result = soup.find_all('div',class_='search-result')


for x in range(len(div_search_result)):
    #title
    title = div_search_result[x].h2.text
    print(f'\n{title}\n')

    #sub head
    sub_header = div_search_result[x].find(class_='search-result-sub-header wrap-text').text
    print(f'{sub_header}\n')

    #wrap text
    wrap_text = div_search_result[x].find_all(class_='wrap-text')[1].text
    print(f'{wrap_text}\n')

    #strong
    strong = div_search_result[x].find_all(class_='search-result-entry')

    for o in range(len(strong)):
        print(strong[o].text)

    #link    
    link = div_search_result[x].h2.a['href']
    print(f'\n{link}\n')
    print("-"*125)


# In[35]:


titles = []
sub_headers=[]
wrap_texts=[]
links=[]
all_strongs = []

for x in range(len(div_search_result)):
    #title
    title = div_search_result[x].h2.text
    titles.append(title)
    
    #sub head
    sub_header = div_search_result[x].find(class_='search-result-sub-header wrap-text').text
    sub_headers.append(sub_header)
    
    #wrap text
    wrap_text = div_search_result[x].find_all(class_='wrap-text')[1].text
    wrap_texts.append(wrap_text)
    
    #strong
    strong = div_search_result[x].find_all(class_='search-result-entry')

    strongs = []
    
    for o in range(len(strong)):
        strongs.append(strong[o].text)
    
    all_strongs.append(strongs)
    #link    
    link = div_search_result[x].h2.a['href']
    links.append(link)


# In[36]:


import pandas as pd ,numpy as np 


# In[37]:


zipped = list(zip(titles,sub_headers,wrap_texts,all_strongs,links))


# In[38]:


csv_file = pd.DataFrame(zipped,columns=['titles','sub_headers','wrap_texts','all_strongs','links'])
csv_file


# In[39]:


csv_file.to_csv('Gov_uk_contractfinder.csv')


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




