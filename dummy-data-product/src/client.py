###### Basic Packages ###########
import pandas as pd

import os
#### Packages From templates #####
from dependencies.standardization.standardizer import Standards
from dependencies.scraping.scraper import Scrapping
from dependencies.cleaning.cleaning import Clean
from dependencies.geocoding.geocoder import Geocode
from dependencies.utils.lookup_utility import Utils


#################################


# =============================================================================
#                               Main Code
# =============================================================================


### Helper Small Functions ###
def data_clean(data):
    data=str(data)
    return data.strip("'[]''")

def strip_data(data):
        data= str(data)
        data= data[data.find('-')+1:].lstrip(" ")
        return data
        
def stripping_column(dataframe):
    column_list=['type_of_buyer','type_of_contract','type_of_procedure','notice_type','regulation','type_of_bid','award_criteria']
    for column_name in column_list:
        dataframe[column_name]=dataframe[column_name].apply(strip_data)
            
    return dataframe
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
                  
         

     for i in range(len(final_dataframe)):
         country_iso=final_dataframe['country_iso'][i]
         town_iso=final_dataframe['town_iso'][i]
         geocode= Geocode(country_iso,town_iso)
         latitude,longitude= geocode.geolocate() 
         final_dataframe.at[i,'latitude']=   latitude
         final_dataframe.at[i,'longitude']=   longitude
     path= os.getcwd()+'/Lookup/'
     util=Utils(final_dataframe,path)
     ## Country MFn Code , ISO alpha and Amount Converted to USD
     final_dataframe= util.country_lookup()
     final_dataframe= util.amount_conversion()
     clean= Clean(final_dataframe)
     clean_dataframe= clean.finding_duplicates()
     clean_dataframe= stripping_column(clean_dataframe)
     ##### Standardizing Dataframe
     standard= Standards(clean_dataframe)
     clean_dataframe= standard.stadardize_data()
     util=Utils(clean_dataframe,path)
     message= util.save_csv(scope,country_name)
     print(message)
except Exception:
    pass