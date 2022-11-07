'''data.csv

'''
#Imports to write the data and write the CSV file.
import requests
import re
from bs4 import BeautifulSoup
from csv import writer

#imports to read the CSV file and draw the Graph.
import matplotlib.pyplot as plt
import pandas as pd

def webscraper():
  url = "https://opentender.eu/start"
  page = requests.get(url)
  
  soup = BeautifulSoup(page.content, 'html.parser')
  results = soup.find_all('li', class_="portal-link")
  
  with open('data.csv', 'w', newline='', encoding='utf8') as f:
    thewriter = writer(f)
    header = ['Country', 'Number of Tenders']
    thewriter.writerow(header)
    for result in results:
      country = result.find('a').text
      tenderNumber = result.find('div').text
      
      #regular expression pattern to get numbers...
      pattern = re.findall("[0-9]", tenderNumber)
      str_pattern = ''.join(pattern)
      integer_tenderNumber = int(str_pattern)
      if integer_tenderNumber < 999:
        datainfo = [country, integer_tenderNumber*100000]
      else:
        datainfo = [country, integer_tenderNumber]
      thewriter.writerow(datainfo)

  #Now Let's focus on the Bar Chart:
  plt.style.use('bmh') #This line isn't necessary. This is only used for the purpose of styling the graph.
  csvFile = pd.read_csv('data.csv')
  
  x = csvFile['Country']
  y = csvFile['Number of Tenders']
  
  #Bar Chart
  plt.xlabel('Tenders #:', fontsize = 18)
  plt.ylabel('Countries: ', fontsize = 16)
  plt.ticklabel_format(style='plain') #This line prevents the scientific notation in the x-axis.
  plt.barh(x,y, color='green', edgecolor='red')

  #Print Graphs
  plt.show()

#driver code:
webscraper()