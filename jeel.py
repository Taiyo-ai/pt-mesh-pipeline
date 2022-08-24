import requests
from bs4 import BeautifulSoup
import csv 
import pandas as pd
url = "https://opentender.eu/all/download"
r = requests.get(url)
htmlContent = r.content
#print(htmlContent) # get all html content
soup = BeautifulSoup(htmlContent, 'html.parser')
#print(soup.prettify)
title = soup.title
#print(title) # get title
#print(type(title))
#print(type(title.string))
paras  = soup.find_all('p')
#print(paras) # get all paragraphs
anchors  = soup.find_all('a')
#print(anchors) #get all anchors
# get all the anchor tags from the page
anchors = soup.find_all('a')
all_links = set()
# get all the links on page:
#for link in anchors:
    #if(link.get('href')  != '#'):
     # link = "https://opentender.eu/all/download" +link.get('herf')
      #all_links.add(link)
      #print(link)
#print(soup.find('p'))# get first element in html page
#print(soup.find('p')['class']) # get classes of any element in html page
#print(soup.find_all("p" , class_="lead")) # get all elements with class lead
#print(soup.find('p').get_text) # get the text from the tags/soup
#print(soup.get_text())

class requiresData:
 url = "https://opentender.eu/all/download"
 r = requests.get(url)
 htmlContent = r.content
 soup2 = BeautifulSoup(htmlContent,'html.parser')
 value = soup2.find_all(attrs={'class': 'container-outer downloads'})
 downloadRow = soup2.find_all(attrs={'class': 'download-row'})
print(requiresData.downloadRow)










