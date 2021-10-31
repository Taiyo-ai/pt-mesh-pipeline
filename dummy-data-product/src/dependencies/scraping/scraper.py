#importing essential libraries

import requests
from bs4 import BeautifulSoup
import re
import dateutil
import pandas as pd
import pycountry

li = [] #empty list to store title of tenders
li2 = []  #empty list to store if it's active or closed
li3 = []  #empty list to store the deadline fo the tenders
li4 = []  #empty list to store the Sectors of the tenders
li5 = []  #empty list to store country
li6 = []  #empty list to store country code
li7 = []  #empty list to store url
li8 = []  #empty list to store source

#there are 1236 pages, but for this assignment I'm considering first 5 pages.
def scrape():
  for i in range(1):
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
      country_val = country.contents[0].split(';')[1]
      li5.append(country_val)
      try:
        code = pycountry.countries.search_fuzzy(country_val)[0].numeric
        li6.append(code)
      except:
        li6.append('NA')
    data['Country'] = li5
    data['country_code'] = li6


  #Adding Map Co-ordinates
  #Since, map co-ordinates aren't given, puttin [] in place.
    data['map_cordinates'] = '[]'

    data['project_or_tender'] = 'T'

    for i in document.find_all('div',{'class':'item-title'}):
      for link in i.find_all('a'):
        url = 'https://www.adb.org'+ link.get('href')
        li7.append(url)
        #scraping source if it's not a pdf file
        if (requests.get(url).url[-3:] != 'pdf'):
          r = requests.get(url)
          re_link = requests.get(r.url)
          scrp = re_link.text
          document1 = BeautifulSoup(scrp, 'lxml')
          for i in document1.find_all('span',{'id':'mcConsultantSource'}):
            source = i.contents[0].contents[0]
            li8.append(source)
        else: #if the file is a pdf file, asigning it a NA string.
          li8.append('NA')
   
    data['url'] = li7
    data['source'] = li8


  return data

print(scrape())
