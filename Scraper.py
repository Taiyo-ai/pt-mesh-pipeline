import pandas as pd
from bs4 import BeautifulSoup
import re
import requests

class Scraper:
  def __init__(self, url):
    self.url = url

  def eprocure(self):
    res = requests.get(self.url)
    res
    soup = BeautifulSoup(res.text, 'html.parser')

    rows1 = []

    table1 = soup.find('table', id = 'activeTenders')
    for tr in table1.find_all('tr'):
      data = tr.find_all('td')
      rows1.append([td.text for td in data])

    df = pd.DataFrame(rows1)

    table2 = soup.find('table', id = 'activeCorrigendums')
    rows2 = []
    for tr in table2.find_all('tr'):
      data = tr.find_all('td')
      rows2.append([td.text for td in data])
      #l = len(df)
      #df.loc[l] = 
    headers = []
    for row in soup.find_all('tr', class_ = 'list_header'):
      data = row.find_all('td')
      headers.append([td.text for td in data])


    df1 = pd.DataFrame(rows1, columns = headers[0])

    df2 = pd.DataFrame(rows2, columns = headers[2])

    df1['Tender Title'] = df1['Tender Title'].apply(lambda x: re.sub('\d. ', '', x))
    df2['Corrigendum Title'] = df2['Corrigendum Title'].apply(lambda x: re.sub('\d. ', '', x))
    return [df1, df2]

  ####################################################################################################

  def cpppc(self):
    res = requests.get(self.url)
    cpppc = BeautifulSoup(res.text, 'html.parser')
    cpppc
    ls = cpppc.find('ul', 'new-content ppp-list')
    rows = []
    for li in ls.find_all('li'):
    # li = ul.find('li')
      a = li.find('a')
      div = li.find('div')
      rows.append([a.text, div.text])

    titles = [rows[i][0] for i in range(len(rows))]
    desc = [rows[i][1] for i in range(len(rows))]
    df3 = pd.DataFrame([titles, desc]).T
    df3.columns = ['Title', 'Description']
    return df3

  ######################################################################################################

  def ggzy(self):
    res = requests.get(self.url)
    ggzy = BeautifulSoup(res.text, 'html.parser')

    div1 = ggzy.find('div', class_ = 'main_list_on')

    try:
      headers1 = []

      for h4 in div1.find_all('h4'):
        headers1.append(h4.text)

      headers1.append('Date')
      rows1 = []
      for ul in div1.find_all('ul'):
        data = ul.find_all('li')
        for li in data:
          link = li.find('a') 
          a = li.find('span')
          rows1.append([link.text, a.text])

      df1 = pd.DataFrame(rows1)
      df1.columns = headers1

    except:
      print('Class NoneType')

    div2 = ggzy.find('div', class_ = 'main_list_on main_list_tw')

    try:
      headers2 = []

      for h4 in div2.find_all('h4'):
        headers2.append(h4.text)

      headers2.append('Date')
      rows2 = []
      for ul in div2.find_all('ul'):
        data = ul.find_all('li')
        for li in data:
          link = li.find('a') 
          a = li.find('span')
          rows2.append([link.text, a.text])

      df2 = pd.DataFrame(rows2)
      df2.columns = headers1
    except:
      print('Class NoneType')
    
    return [df1,df2]
