
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'}

data3 = []

def fulldata(tag):
    url='https://www.contractsfinder.service.gov.uk/Search/Results?&page={tag}#dashboard_notices'

    r = requests.get(url, headers=headers)

    soup = BeautifulSoup(r.content, 'html.parser')

    data = soup.find_all('div', {'class':'search-result'})

    for item in data:
        data2= {
        'title' : item.find('div', {'class':'search-result-header'})['title'],
        'governing_body' : item.find('div',{'class':'search-result-sub-header wrap-text'}).text,
        'procurement' : item.find("div",{'class':'search-result-entry'}).text
        }
        data3.append(data2)
    return
for x in range(1,3):
    fulldata(x)

    

    
df = pd.DataFrame(data3)

df.to_csv('Assesment.csv')

print('finish')
    
   
    

    
    
    
    
    
    

    
   


   