

from zipfile import ZipFile
import pandas as pd
import requests
import json
import os

class Cleaning:
    def __init__(self):
        # reading and loading data from config.json
        with open('./config.json') as file:
            data = json.load(file)
        self.output_name = data['output_csv']
        self.df = None
        
        # reading the data csv file
        self.df = pd.read_csv('../data/' + self.output_name, encoding='utf-16', delimiter='\t')

        # gathering currency exchange rate data
        url = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip?2f79b933fe904f0b1c88df87fe70ddd7'
        response = requests.get(url)
        open("./dependencies/cleaning/rates.zip", "wb").write(response.content)
        with ZipFile("./dependencies/cleaning/rates.zip", 'r') as file:
            file.extractall(path="./dependencies/cleaning/")
        os.remove('./dependencies/cleaning/rates.zip')
        self.rates = pd.read_csv('./dependencies/cleaning/eurofxref-hist.csv', usecols=['Date','USD','INR'])
        self.rates['Date'] = pd.to_datetime(self.rates['Date'], errors='coerce')
        self.rates['rate'] = self.rates['INR']/self.rates['USD']
        
    def __inr_to_usd(self,column):
        for i in range(len(self.df)):
            date = self.df.loc[i,'Published Date'].day
            month = self.df.loc[i,'Published Date'].month
            year = self.df.loc[i,'Published Date'].year
            rate = self.rates[(self.rates['Date'].dt.day == date) & (self.rates['Date'].dt.month == month) & (self.rates['Date'].dt.year == year)]['rate']

            if rate.empty or rate.isna().values[0]:
                rate = self.rates[(self.rates['Date'].dt.year == year)]['rate'].mean()
            else:
                rate = rate.values[0]
            if self.df.loc[i,column] != 'NA':
                self.df.loc[i,column] = round(float(self.df.loc[i,column]) / float(rate),2)
    
    def __fill_null(self,value='NA'):
        self.df.fillna(value)
    
    def __replace_substr(self,column,val,replace_with=""):
        self.df[column] = [i.replace(val,replace_with) if isinstance(i, str) else i for i in self.df[column]]
        
    def __datetime(self,column):
        self.df[column] = pd.to_datetime(self.df[column], errors='coerce')
    
    def cleaning(self):
        # filling null values
        self.__fill_null()
        
        # replacing unnecessary values
        self.__replace_substr('Tender Value in Dollars',",")
        self.__replace_substr('Tender Fee in Dollars',",")
        self.__replace_substr('EMD Percentage',"%")
        self.__replace_substr('EMD Amount in Dollars',",")
        
        
        
        # converting dates to datetime format
        self.__datetime('Published Date')
        self.__datetime('Bid Opening Date')
        self.__datetime('Document Download / Sale Start Date')
        self.__datetime('Document Download / Sale End Date')
        self.__datetime('Bid Submission Start Date')
        self.__datetime('Bid Submission End Date')
        
        
        
        # converting currency from INR to USD
        self.__inr_to_usd('Tender Fee in Dollars')
        self.__inr_to_usd('EMD Amount in Dollars')
        self.__inr_to_usd('Tender Value in Dollars')
        
    def saving(self):
        self.df.to_csv('../data/' + self.output_name, encoding='utf-16',sep='\t', index=False)
        
    def cleanup(self):
        os.remove('./dependencies/cleaning/eurofxref-hist.csv')
        


# In[ ]:




