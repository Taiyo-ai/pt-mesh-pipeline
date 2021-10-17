###### Basic Packages ###########
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
import requests
import json
import base64
import time
from geopy.geocoders import Nominatim
import csv
import glob
import os
#### Packages From templates #####
from dependencies.scraping.scraper import Scrapping
from dependencies.cleaning.cleaning import *
from dependencies.geocoding.geocoder import Geocode
from dependencies.utils.lookup_utility import Utils


#################################


# =============================================================================
#                               Main Code
# =============================================================================



### Initail Variables

## country_name= IN,FR,UK,US etc
### scope: Searching Docid for status
## 1:- Inactive Tender
## 2 :-Active Tender
## 3:- ALL
## count:- No of Doc ID to get  eg 40 50 80 etc Numeric value

country_name= input('Enter Country Symbol:- ')
scope= int(input('Enter Scope Value:- '))
count= int(input('Enter Number of Doc-id to Fetch:- '))
final_list= []

### creating Objects #####
scrapper= Scrapping(country_name,scope,count)

document_id_list= scrapper.get_doc_id_list()
for doc_id in document_id_list:
    xml_data= scrapper.get_decoded_xml(doc_id)
    data= scrapper.get_xml_data(xml_data,doc_id)
    final_list.append(data)

    
try:
     final_dataframe=pd.concat(final_list, axis=0, ignore_index=True)
     column_list= list(final_dataframe.columns)
     for column_name in column_list:
         final_dataframe[column_name]= final_dataframe[column_name].apply(data_clean)
       
     path= os.getcwd()+'/Lookup/'
     util=Utils(final_dataframe,path)
     ## Country MFn Code , ISO alpha and Amount Converted to USD
     final_dataframe= util.country_lookup()
     final_dataframe= util.amount_conversion()
     clean= Clean(final_dataframe)
     final_dataframe= clean.finding_duplicates()
     message= util.save_csv(scope,country_name)
     print(message)
except Exception:
    pass