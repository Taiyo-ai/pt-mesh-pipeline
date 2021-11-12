import bs4
from bs4 import BeautifulSoup
import requests
from requests_html import HTMLSession
import math

s = HTMLSession()
html_info_ = requests.get('https://fred.stlouisfed.org/categories/22').text

soup1 = BeautifulSoup(html_info_, 'lxml')

links_with_duplicates = []
for a in soup1.find_all('a', href=True):
    if "/categories/" in a['href']:
        links_with_duplicates.append(a['href'])

links_ = [] #removing deuplicates
for x in links_with_duplicates:
    if x not in links_:
        links_.append(x)

# print(links_)


def scrapeData(url):
    r = s.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup



def nextPage(precSoup):
    if precSoup.find('a', {"title":"next page"}):
        url = precSoup.find('a', {"title":"next page"})['href']
        return url, nextPage(scrapeData(url))


all_links = []
for i in range(len(links_)):
    all_links.append("https://fred.stlouisfed.org" + str(links_[i]))
    all_links.append(nextPage(scrapeData("https://fred.stlouisfed.org" + links_[i])))
    # print(all_links)

print(len(all_links), all_links)
