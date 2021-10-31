#importing essential libraries

import requests
from bs4 import BeautifulSoup
import re
import dateutil
import pandas as pd

li = [] #empty list to store title of tenders
li2 = []  #empty list to store if it's active or closed
li3 = []  #empty list to store the deadline fo the tenders
li4 = []  #empty list to store the Sectors of the tenders
li5 = []

#there are 1236 pages, but for this assignment I'm considering first 5 pages.
def scrape():
  for i in range(5):
    result = requests.get('https://www.adb.org/projects/tenders?page='+str(i))
    src = result.text
    document = BeautifulSoup(src, 'lxml')
    for table in document.find_all("div", {"class": "item-title"}):
      li.append(table.contents[0])
      if (table.contents[0] == '\n'):
        li.pop()      #popping new lines
    data = pd.DataFrame({'Name':li})

  #finding Activeness. It can have following values: ACTIVE, CLOSED, AWARDED, ARCHIVED, etc.
    for i in document.find_all('div',{'class':'item-meta'}):
      li2.append(i.contents[1].contents[2].contents[0])
    data['Status'] = li2

  #Scraping from summary, the time and date of the posting/contracting date.
    for i in document.find_all('div',{'class':'item-summary'}):
      start =  (i.contents[0].find('date'))
      li3.append(i.contents[0][start+len('date:'):])
    data['Date'] = li3

  #Scraping from summary, the Sectors of tenders
    for sector in document.find_all('div',{'class':'item-summary'}):
      try:
        li4.append(sector.contents[0].split(';')[2])
      except IndexError:
        li4.append('NA')
    data['Sector'] = li4

    for country in document.find_all('div',{'class':'item-summary'}):
      li5.append(country.contents[0].split(';')[1])
    data['Country'] = li5

  return data
