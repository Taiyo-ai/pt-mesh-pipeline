# -*- coding: utf-8 -*-
"""
Created on Thu Dec 15 19:08:52 2022

@author: sudeepthikanth
"""
###Scrapping##
from bs4 import BeautifulSoup#importing beautiful soup#
import requests#import requests
import pandas as pd#import pandas

url= "https://opentender.eu/start"##page url#
page = requests.get(url)#requesting page url#
soup = BeautifulSoup(page.content ,'html.parser')##
###extracting countries and number of tenders##
countries=[]
for country in soup.find_all('ul', class_="portal-links"):
   countries.append(country.text.replace('\n',' ').split()) 
   print(countries)
   res = country.text.replace(' ','').split()
##extracting urls from the page##
links=[]       
for link in soup.find_all('a'):
    links.append(link.get('href'))
    print(links)
##converting lists into dataframe##
dfcountry= pd.DataFrame({'tenders':res}) 
dflinks=pd.DataFrame({'links':links}) 
##Data cleaning##
##splitting countries and number of tenders to seperate columns## 
country=dfcountry.iloc[::2]##splitting countries##
countries=country.reset_index(drop=True)##resetting index##
countries.rename(columns = {'tenders':'Countries'}, inplace = True)##renaming column name##
tendersnumber=dfcountry.iloc[1::2]##splitting number of tenders##
tendersnumber=tendersnumber.reset_index(drop=True)##resetting index##
tendersnumber.rename(columns = {'tenders':'numberoftenders'}, inplace = True)##renaming column name##
dflinks.drop(dflinks.loc[0:5].index, inplace=True)##dropping rows range from 0-5##
dflinks.drop(dflinks.loc[39:79].index, inplace=True)##dropping rows range from 39-79##
tenderlinks=dflinks.reset_index(drop=True)##resetting index##
result = pd.concat([countries, tendersnumber,tenderlinks], axis=1, join='inner')##concating dataframe##
result.numberoftenders = result.numberoftenders.str.replace(",","")###replacing comma##
result.numberoftenders=result.numberoftenders.replace( {"Million":"*1e6"}, regex=True).map(pd.eval).astype(int)##converting million to integer ##
### convert to csv format##
result.to_csv('tenders.csv', index=False, encoding='utf-8')
###Data visualization##
import seaborn as sns ##import seaborn##
import matplotlib.pyplot as plt##import matplotlib##
##UNIVARIATE##
sns.histplot(x=result.numberoftenders,data=result)##plotting number of tenders ###

##BIVARIATE##
fig = plt.gcf()
sns.scatterplot( x=result.Countries, y=result.numberoftenders, data=result,hue=result.numberoftenders)##plotting number of tenders with countries ##
fig.set_size_inches(30, 10)##resizing image##

