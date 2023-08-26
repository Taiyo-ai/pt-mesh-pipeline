# import your dependencies here

import pandas as pd
import requests
from zipfile import ZipFile
from io import BytesIO
import numpy as np
import os

class CleanigData:
    def __init__(self, **kwargs):

        self.csvfile = kwargs.get("csvfile")
        self.df = None
        self.rates = None
        # read data from csv
        self.output_file = 'cleaned_' + self.csvfile
        self.df = pd.read_csv("../../data/" + self.csvfile , encoding='utf-16', delimiter='\t')
        self.url = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip?2f79b933fe904f0b1c88df87fe70ddd7'

    def __load_exchange_rates(self):
        # Make a GET request to the specified URL to fetch the data
        response = requests.get(self.url)

        # Extract the content of the downloaded zip file
        with ZipFile(BytesIO(response.content)) as zip_file:
            # Open the CSV file within the zip archive
            with zip_file.open('eurofxref-hist.csv') as csv_file:
                # Read the CSV data using pandas, selecting only the specified columns
                self.rates = pd.read_csv(csv_file, usecols=['Date', 'USD', 'INR'])

                # Convert the 'Date' column to datetime format, handling errors by coercing invalid values
                self.rates['Date'] = pd.to_datetime(self.rates['Date'], errors='coerce')

                # Calculate the exchange rate by dividing INR by USD and store it in the 'rate' column
                self.rates['rate'] = self.rates['INR'] / self.rates['USD']

    def __get_exchange_rate(self, day , month , year):
        # get exchange rate
        # Extract rates for the given day, month, and year
        rate = self.rates[
            (self.rates['Date'].dt.day == day) &
            (self.rates['Date'].dt.month == month) &
            (self.rates['Date'].dt.year == year)
        ]['rate']

        # Check if the extracted rate is empty or contains NaN values
        if rate.empty or rate.isna().values[0]:
            # Calculate the average rate for the entire year if conditions aren't met
            rate = self.rates[self.rates['Date'].dt.year == year]['rate'].mean()
        else:
            # Use the specific rate value if it's valid
            rate = rate.values[0]

        # Return the calculated rate
        return rate

    def __convert_currency(self):
        # Conversion of amounts to USD

        for index, row in self.df.iterrows():
            date = row['Published Date']  # Adjust the column name as needed
            tender_value = row['Tender Value in Dollars']   # Adjust the column name as needed
            tender_fee = row['Tender Fee in Dollars']  # Adjust the column name as needed
            EMD_value = row['EMD Amount in Dollars']  # Adjust the column name as needed
            if not pd.isnull(date) and not pd.isna(date):
                day , month , year = pd.to_datetime(date).day , pd.to_datetime(date).month , pd.to_datetime(date).year
                exchange_rate = self.__get_exchange_rate(day , month , year)

                if exchange_rate is not None:
                    self.df.at[index, 'Tender Value in Dollars'] = round(tender_value / exchange_rate , 2) if tender_value != 'NA' else 'NA'
                    self.df.at[index, 'Tender Fee in Dollars'] = round(tender_fee / exchange_rate , 2) if tender_fee != 'NA' else 'NA'
                    self.df.at[index, 'EMD Amount in Dollars'] = round(EMD_value / exchange_rate , 2) if EMD_value != 'NA' else 'NA'

    def __replace_str(self):
        # replace "," and '%' with "" in amounts and convert into float

        self.df['Tender Value in Dollars'] = self.df['Tender Value in Dollars'].apply(lambda x : x if x == 'NA' else float(x.replace(',', '')))
        self.df['Tender Fee in Dollars'] = self.df['Tender Fee in Dollars'].apply(lambda x : x if x == 'NA' else float(x.replace(',', '')))
        self.df['EMD Percentage'] = self.df['EMD Percentage'].str.replace('%', '')
        self.df['EMD Amount in Dollars'] = self.df['EMD Amount in Dollars'].apply(lambda x : x if x == 'NA' else float(x.replace(',', '')))

    def __fill_null(self , value='NA'
                    ):

        # fill null value with 'NA'
        self.df.fillna('NA', inplace=True)

        # for date fields has null value
        self.df = self.df.applymap(lambda x: 'NA' if pd.isnull(x) or x is None or str(x).strip() == '' else x)

        # replace "," with "" in amounts
        self.__replace_str()

    def __fill_null_date_value(self):
        self.df = self.df.applymap(lambda x: 'NA' if pd.isnull(x) or x is None or str(x).strip() == '' else x)
        null_count = self.df.isnull().sum().sum()
        if null_count == 0:
            print("No Null values found")

    def __parse_date(self):
        # Parsing date columns

        date_columns = ['Published Date', 'Bid Opening Date', 'Document Download / Sale Start Date',
                        'Document Download / Sale End Date', 'Clarification Start Date', 'Clarification End Date',
                        'Bid Submission Start Date', 'Bid Submission End Date', 'Pre Bid Meeting Date']

        for column in date_columns:
            self.df[column] = pd.to_datetime(self.df[column], errors='coerce', format='%d-%b-%Y %I:%M %p')
        self.__fill_null_date_value()

    def __remove_duplicate(self):
        # remove duplicates value
        self.df.drop_duplicates(inplace=True)

    def clean_data(self):
        """Do extraction or processing of data here"""
        self.__fill_null()

    def save_data(self):
        """Function to save data"""

        self.df.to_csv("../../data/" + self.output_file , encoding="utf-16" , sep='\t' , index=False)

    def run(self):
        """Load data, do_something and finally save the data"""
        print("Inside Cleaning Data Module")

        self.__load_exchange_rates()
        self.clean_data()
        self.__convert_currency()
        self.__remove_duplicate()
        self.__parse_date()
        self.save_data()

