import requests
from scrapper import Scrapper
from bs4 import BeautifulSoup
def results(url):

  res = requests.get(url)
  if str(res) != '<Response [200]>':
    df = 'Not Allowed'

  else: 
    soup = BeautifulSoup(res.text, 'html.parser')
    #checking all the links throught their tags and classname or id
    res1 = soup.find_all('table', id = 'activeTenders')
    res2 = soup.find_all('ul', 'new-content ppp-list')
    res3 = soup.find_all('div', class_ = 'main_list_on')

    if len(res1) != 0 and len(res2) == 0 and len(res3) == 0:
      df = Scrapper(url).etender()

    elif len(res1) == 0 and len(res2) != 0 and len(res3) == 0:
      df = Scrapper(url).cppc()

    elif len(res1) == 0 and len(res2) == 0 and len(res3) != 0:
      df = Scrapper(url).ctender()

    else: 
      df = 'None'

  return df
