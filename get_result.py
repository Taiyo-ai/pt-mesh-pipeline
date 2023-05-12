import requests
from Scraper import Scraper
from bs4 import BeautifulSoup
def get_result(url):

  res = requests.get(url)
  if str(res) != '<Response [200]>':
    df = 'Not Allowed'

  else: 
    soup = BeautifulSoup(res.text, 'html.parser')
    res1 = soup.find_all('table', id = 'activeTenders')
    res2 = soup.find_all('ul', 'new-content ppp-list')
    res3 = soup.find_all('div', class_ = 'main_list_on')

    if len(res1) != 0 and len(res2) == 0 and len(res3) == 0:
      df = Scraper(url).eprocure()

    elif len(res1) == 0 and len(res2) != 0 and len(res3) == 0:
      df = Scraper(url).cpppc()

    elif len(res1) == 0 and len(res2) == 0 and len(res3) != 0:
      df = Scraper(url).ggzy()

    else: 
      df = 'None'

  return df
