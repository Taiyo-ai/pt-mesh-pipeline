#!/usr/bin/env python
# coding: utf-8


import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.64'}
# Send a request to the website and get the response
response = requests.get('https://www.chinabidding.com/en/info/search.htm', headers=headers)
if response.status_code != 200:
    print('Error: Unable to access the website')
    exit()

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(response.content, 'lxml')
new_tenders_section = soup.find('div', {'class': 'result-con'})
if new_tenders_section is None:
    print('Error: Unable to find the New Tenders section')
    exit()

new_tender_items = new_tenders_section.find_all('li', attrs={'class': 'list-item'})
if not new_tender_items:
    print('Error: Unable to find any tender cards')
    exit()

new_tenders_data = []
for item in new_tender_items:
    try:
        title = item.find('div', {'class': 'item-title clearfix'}).find('a').text.strip()
        description = item.find('div', {'class': 'item-content px14'}).text.strip()
        industry = item.find('div', {'class': 'item-link'}).find_all('span')[0].text.strip()
        region = item.find('div', {'class': 'item-link'}).find_all('span')[1].text.strip()
    except AttributeError as e:
        print(f'Error: Unable to extract data from card ({e})')
        continue
    
    new_tenders_data.append({
        'Title': title,
        'Description': description,
        'Industry': industry,
        'Region': region
    })

if not new_tenders_data:
    print('Error: Unable to extract any tender data')
    exit()

df = pd.DataFrame(new_tenders_data)
##print(df)
df.to_csv('New_Tenders_data.csv', sep=',', index=False,header=True)





