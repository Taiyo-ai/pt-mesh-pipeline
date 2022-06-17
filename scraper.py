import requests
from bs4 import BeautifulSoup

def scraper(url, cls):
    cl = []
    r = requests.get(url, headers={"User-Agent": "XY"})
    soup = BeautifulSoup(r.content, 'html.parser')
    #print(soup.prettify())
    s = soup.find('div', class_= cls)
    options = s.find_all("option")
    for option in options:
        tbl = s.find('tbody')
        rows = tbl.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            cl.append(cols)


    return cl
