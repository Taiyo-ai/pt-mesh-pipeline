
import numpy as np
import pandas as pd
import requests
import time
import csv
import glob
import os

class Utils:
    
    def __init__(self,dataframe,path):
        self.dataframe=dataframe
        self.path=path

    def country_lookup(self):
        dataframe=self.dataframe
        country_iso=[]
        country_mfn=[]
        currency_code=[]
        country_table=pd.read_csv(self.path+'Country_list.csv')
        currency_table=pd.read_csv(self.path+'Currency.csv')
        for i in range(len(dataframe)) :
            try:
                country_name= str(dataframe.loc[i, "country_iso"])
                iso_country_code= str(country_table.loc[ country_table['Country'].str.lower() == country_name.lower(),'Alpha-3 code'].values).strip('[ ]')
                iso_country_code=iso_country_code.replace("'","")
                iso_country_code= iso_country_code.replace('"',"")
                
                iso_country_mfn= str(country_table.loc[country_table['Country'].str.lower() == country_name.lower(),'Numeric code'].values).strip('[ ]')
                iso_country_mfn=iso_country_mfn.replace("'","")
                iso_country_mfn= iso_country_mfn.replace('"',"")
                
                currency= str(currency_table.loc[currency_table['Entity'].str.lower() == country_name.lower(),'AlphabeticCode'].values).strip('[ ]')
                currency=currency.replace("'","")
                currency = currency.replace('"',"")
               
    # =============================================================================
    #             country_iso.insert(i,iso_country_code)
    #             country_mfn.insert(i,iso_country_mfn)
    #             currency_code.insert(i,currency)
    # =============================================================================
                dataframe.at[i,'country_alpha']= iso_country_code
                dataframe.at[i,'country_mfn']= iso_country_mfn
                dataframe.at[i,'currency_code']= currency
            except:
                country_iso.insert(i,np.nan)
                country_mfn.insert(i,np.nan)
                currency_code.insert(i,np.nan)
                continue
    
    
        return dataframe
    
    
    
    
    
    
    def amount_conversion(self):
        dataframe=self.dataframe
        api_key='8d4edafb83dc04bc5bc3'
        #country_code='INR'  
        url='https://free.currconv.com/api/v7/convert?q=USD_{0}&compact=ultra&apiKey={1}'
        
        for i in range(len(dataframe)):
            try:
                currency_code= dataframe.loc[i, "currency_code"]
                amount= dataframe.loc[i, "amount"]
                
                if amount is None:
                    dataframe.at[i,'converted_amount_usd']=amount
                    
                else:
                    
                    if currency_code=='USD':
                        dataframe.at[i,'converted_amount_usd']=amount
               
                    else:
                        api_amount=requests.get(url.format(currency_code,api_key)).json()
                        key= 'USD_' + currency_code
                        api_amount=float(api_amount[key])
                        converted_amount= float(amount)/api_amount
                        dataframe.at[i,'converted_amount_usd']= round(converted_amount,4)
                        
            except:
                    dataframe.at[i,'converted_amount_usd']=np.nan
                    continue
                
        return dataframe
    
    
    def save_csv(self,scope,country_name):
        dataframe=self.dataframe
        try:
            timestamp = time.time()
            filename= country_name + '_' + str(scope) + '_' + str(timestamp) + '.csv'
            dataframe.to_csv(filename, index=False, header=True)
            return 'Sucessfully Save'
        except Exception:
            return 'Failed To Save'
        
    
    def merging_whole_df(self):
        filenames = [i for i in glob.glob("*.csv")]
        header_keys = []
        merged_rows = []
    
        for filename in filenames:
            with open(filename) as f:
                reader = csv.DictReader(f)
                merged_rows.extend(list(reader))
                header_keys.extend([key for key in reader.fieldnames if key not in header_keys])
    
        with open("combined.csv", "w") as f:
            w = csv.DictWriter(f, fieldnames=header_keys)
            w.writeheader()
            w.writerows(merged_rows)
                
            
                
            
            
