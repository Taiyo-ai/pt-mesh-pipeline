import pandas as pd
import re
import requests
from bs4 import BeautifulSoup

from dependencies.scraping import scraper
from dependencies.cleaning import cleaner
from dependencies.standardization import standardizer

u = 'https://www.publiccontractsscotland.gov.uk/search/search_mainpage.aspx'
c = 'col-xl-8 col-lg-8 col-md-7 col-sm-12 ns-list-main'


clst = scraper(u, c)
df2 = cleaner(clst)
df2['Date'] = standardizer(df2['Date'])
df2['Deadline_Date'] = standardizer(df2['Deadline_Date'])

#df2.head()
df2.to_excel("output.xlsx")