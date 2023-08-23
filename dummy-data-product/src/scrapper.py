import pandas as pd
from bs4 import BeautifulSoup
import re
import requests

class Scrapper:
    def __init__(self, url):
        self.url = url
#Goverment of India tenders
    def etender(self):
        res = requests.get(self.url)
        soup = BeautifulSoup(res.text,'html.parser')    

        rows1=[]
        #scrapping activetenders table
        table1 = soup.find('table', id = 'activeTenders')
        for tr in table1.find_all('tr'):
            data = tr.find_all('td')
            rows1.append([td.text for td in data])

        df = pd.DataFrame(rows1)

        #scrapping corrigendums table

        table2 = soup.find('table', id = 'activeCorrigendums')
        rows2 = []
        for tr in table2.find_all('tr'):
            data = tr.find_all('td')
            rows2.append([td.text for td in data])


        headers = []
        for row in soup.find_all('tr', class_ = 'list_header'):
             data = row.find_all('td')
             headers.append([td.text for td in data])

        df1 = pd.DataFrame(rows1, columns = headers[0])

        df2 = pd.DataFrame(rows2, columns = headers[2])     

        #seprating the digits coming along with the title

        df1['Tender Title'] =  df1['Tender Title'].apply(lambda x: re.sub('\d. ', '' , x))
        df2['Corrigendum Title'] = df2['Corrigendum Title'].apply(lambda x: re.sub('\d. ', '', x))

        #returning dataframes

        return [df1, df2]
    
    #Chinese partnership centres

    def cppc(self):
        res = requests.get(self.url)
        cp = BeautifulSoup(res.text,'html.parser')
        list = cp.find('ul', 'new-content ppp-list')
        rows = []
        #scraping list items 
        for li in list.find_all('li'):
            #scraping anchor tag(Heading) for each content 
            #scraping metadata for each content
            a = li.find('a')
            div = li.find('div')
            rows.append([a.text, div.text])
        #Making title and description as seperate entity list in a dictionary and then making a dataframe of them
        dict1={"title": [rows[i][0] for i in range(len(rows))] , "desc":[rows[i][1] for i in range(len(rows))]}
        df3 = pd.DataFrame(dict1)
        df3.columns = ['Title', 'Description']
        return df3

    #Chinese tenders

    def ctender(self):
        res = requests.get(self.url)
        ct = BeautifulSoup(res.text, 'html.parser')

        div1 = ct.find('div', class_ = 'main_list_on')

        headers1 = []

        h4=div1.find('h4')
        headers1.append(h4.text[:4]) #its including span text too so taking only 4 letters

        headers1.append('Date')

        rows1 = []
        for ul in div1.find_all('ul'):
            data = ul.find_all('li')
            for li in data:
                link = li.find('a') #link extraction
                a = li.find('span') #date extraction
                rows1.append([link.text, a.text])

        df4 = pd.DataFrame(rows1)
        df4.columns = headers1

        #scraping the right side table

        div2 = ct.find('div', class_ = 'main_list_on main_list_tw')    

        headers2 = []

        h4_=div2.find('h4')
        headers2.append(h4_.text[:4]) #its including span text too so taking only 4 letters

        headers2.append('Date')

        rows2 = []
        for ul_ in div2.find_all('ul'):
            data_ = ul_.find_all('li')
            for li_ in data_:
                link_ = li_.find('a') #link extraction
                a_ = li_.find('span') #date extraction
                rows2.append([link_.text, a_.text])

        df5 = pd.DataFrame(rows2)
        df5.columns = headers2

        return [df4,df5]





