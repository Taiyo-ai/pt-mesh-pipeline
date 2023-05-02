import pandas as pd
import re

class DataCleaner:
    def __init__(self, df):
        self.df = df
    
    def clean_data(self):
        #Removing unwanted rows 
        self.df.drop([0,1], inplace=True)
        self.df = df.reset_index(drop=True)
        #Renaming columns
        headers = self.df.iloc[0]
        self.df  = pd.DataFrame(df.values[1:], columns=headers)
        #Remove serial numbers from title
        regex_pat = re.compile(r'([0-9]+[,.])', flags=re.IGNORECASE)
        self.df['Tender Title']=self.df["Tender Title"].str.replace(regex_pat, '', regex=True)
        
        # Rename columns
        self.df.rename(columns={'Tender Title': 'tender_title',
                                'Reference No': 'reference_no',
                                'Closing Date': 'closing_date',
                                'Bid Opening Date': 'bid_opening_date'}, inplace=True)
        
        # Remove special characters from the title
        self.df['tender_title'] = self.df['tender_title'].apply(lambda x: re.sub('[^A-Za-z0-9\s]+', '', x))
        
        # Convert date columns to datetime format
        self.df['closing_date'] = pd.to_datetime(self.df['closing_date'])
        self.df['bid_opening_date'] = pd.to_datetime(self.df['bid_opening_date'])
        
        # Reset index
        self.df.reset_index(drop=True, inplace=True)
        
        return self.df
