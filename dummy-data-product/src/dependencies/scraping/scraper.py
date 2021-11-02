#importing essential libraries

import requests
from bs4 import BeautifulSoup
import re
import dateutil
import pandas as pd
import pycountry

#initiatin global variables
li = [] #empty list to store title of tenders
li2 = []  #empty list to store if it's active or closed
li3 = []  #empty list to store the deadline fo the tenders
li4 = []  #empty list to store the Sectors of the tenders
li5 = []  #empty list to store country
li6 = []  #empty list to store country code
li7 = []  #empty list to store url
li8 = []  #empty list to store source
li9 = []  #empty list to store budget

#there are 1236 pages, but for this assignment I'm considering first 5 pages.

class scraping:

  def __init__(self, **kwargs):
    self.config = kwargs.get("config")

  def scrape(self):
    for i in range(2):
      result = requests.get('https://www.adb.org/projects/tenders?page='+str(i))
      src = result.text
      document = BeautifulSoup(src, 'lxml')

      #finding title
      for table in document.find_all("div", {"class": "item-title"}):
        li.append(table.contents[0])
        if (table.contents[0] == '\n'):
          li.pop()      #popping new lines

      #finding Activeness. It can have following values: ACTIVE, CLOSED, AWARDED, ARCHIVED, etc.
      for i in document.find_all('div',{'class':'item-meta'}):
        li2.append(i.contents[1].contents[2].contents[0])
      
      #Scraping from summary, the time and date of the posting/contracting date.
      for i in document.find_all('div',{'class':'item-summary'}):
        start =  (i.contents[0].find('date'))
        li3.append(i.contents[0][start+len('date:'):])

      #Scraping from summary, the Sectors of tenders
      for sector in document.find_all('div',{'class':'item-summary'}):
        try:
          li4.append(sector.contents[0].split(';')[2])
        except IndexError:
          li4.append('NA')

      #scraping the country code and name
      for country in document.find_all('div',{'class':'item-summary'}):
        country_val = country.contents[0].split(';')[1]
        li5.append(country_val)
        try:
          code = pycountry.countries.search_fuzzy(country_val)[0].numeric
          li6.append(code)
        except:
          li6.append('NA')


      #Adding Map Co-ordinates
      #Since, map co-ordinates aren't given, puttin [] in place.
      #scraping consultant source and budget
      for i in document.find_all('div',{'class':'item-title'}):
        for link in i.find_all('a'):
          url = 'https://www.adb.org'+ link.get('href')
          li7.append(url)
          #print(url)
          #scraping source if it's not a pdf file
          if (requests.get(url).url[-3:] != 'pdf'):
            r = requests.get(url)
            re_link = requests.get(r.url)
            scrp = re_link.text
            document1 = BeautifulSoup(scrp, 'lxml')
            if (document1.find_all('span',{'id':'mcConsultantSource'})):
              for i in document1.find_all('span',{'id':'mcConsultantSource'}):
                source = i.contents[0].text
                li8.append(source)
            else:
              li8.append('NA')
          #scraping budget, if the file isn't PDF. 
            if (document1.find_all('span',{'id':'mstBudgetAmount'})):
              for j in document1.find_all('span',{'id':'mstBudgetAmount'}):
                budget = j.contents[0]
                li9.append(budget)
            else:
                li9.append('NA')
          else: #if the file is a pdf file, asigning it a NA string.
            li8.append('NA')
            li9.append('NA')
            
      data = pd.DataFrame({'Name':li})
      data['Status'] = li2
      data['Date'] = li3
      data['Sector'] = li4
      data['Country'] = li5
      data['country_code'] = li6
      data['map_cordinates'] = '[]'
      data['project_or_tender'] = 'T'   #scraping only tender data for this project
      data['url'] = li7
      data['source'] = li8
      data['budget'] = li9
    return data

  def run(self):
    output = self.scrape()
    return (output.to_csv('adb.csv', index = False))

if __name__ == "__main__":
  config = {}
  obj = scraping(config = config)
  result = obj.run()
