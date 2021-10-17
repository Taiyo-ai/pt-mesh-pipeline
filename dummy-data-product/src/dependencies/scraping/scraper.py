from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
import requests
import json
import base64
import time
from geopy.geocoders import Nominatim
from ..geocoding.geocoder import Geocode
import csv
import glob






class Scrapping:
    
    def __init__(self,country_name,scope,count):
        self.country_name=country_name
        self.scope=scope
        self.count=count
        
        
    def get_doc_id_list(self):    
        url='https://ted.europa.eu/api/v2.0/notices/search?fields=ND&pageSize={2}&q=CY%3D%5B{0}%5D&reverseOrder=true&scope={1}&sortField=ND'.format(self.country_name,self.scope,self.count)
        r = requests.get(url)
        document_id_list= r.json()
        latest_document_list=document_id_list['results']
        document_id_list=[]

        for dict_data in latest_document_list:
            document_id_list.append(dict_data['ND'])
        
        return document_id_list
    




########## XML DOwnload from the list of DOC  ######

#### Parameter List ######
##
##doc_id= Unique doc id
##
###########################

    def get_decoded_xml(self,doc_id):
    #doc_id='520807-2021'
        url='https://ted.europa.eu/api/v2.0/notices/search?fields=CONTENT&q=ND%3D%5B{0}%5D&reverseOrder=true&scope=3&sortField=ND'.format(doc_id)
        r = requests.get(url)
        xml_data=r.json()
        xml_data= xml_data['results']
        xml_data=xml_data[0]
        xml_data=xml_data['content']
        xml_data= base64.b64decode(xml_data)  
        return xml_data






######## Fetch Data and Return DataFrame ###################
## xml_data Byte format xml data to be loaded in Beautiful Soup
## doc_id doc_id number of xml file which we are going to scrap the data
############################

    def get_xml_data(self,xml_data,doc_id):
        scope=self.scope
        
        if scope ==1:
            scope='Inactive'
        elif scope==2:
            scope='Active'
        else:
            scope='Any'
            
        final_data = pd.DataFrame()
        soup = BeautifulSoup(xml_data, 'xml')
        try:   
            final_data.at[0,'doc_id']= doc_id
            final_data.at[0,'notice_status']=scope
            cpv_code= soup.find('cpv_main')
            cpv_code= str(cpv_code)
            cpv_code =''.join(filter(lambda i: i.isdigit(), cpv_code ))
            final_data.at[0,'cpv_code']= cpv_code
            
            reception_id= soup.find('reception_id')
            reception_id_data =reception_id.get_text() 
            final_data.at[0,'reception_id']= reception_id_data
            
        
        except Exception :
            pass    
            
        
        ### Checking For Existence of Doc Fields
        basic_data= soup.find('ML_TI_DOC')   
        try:
            if basic_data:
                country_iso=soup.find("ML_TI_DOC", { "LG" : "EN" }).find("TI_CY", recursive=True)
                country_iso= country_iso.get_text() 
                town=soup.find("ML_TI_DOC", { "LG" : "EN" }).find("TI_TOWN", recursive=True)
                town= town.get_text()  
                project_name=soup.find("ML_TI_DOC", { "LG" : "EN" }).find("TI_TEXT", recursive=False)
                project_name= project_name.get_text()           
                ### Appending Data ####
                final_data.at[0,'country_iso']= country_iso
                final_data.at[0,'town_iso']=  town
                final_data.at[0,'project_name']= project_name
            else:
                pass
        
        except Exception:
            pass   
        
        #### Checking For Form Data Fields
        form_data= soup.find('F03_2014')   
        try:
            if form_data:    
                description= soup.find("F03_2014", { "CATEGORY":"ORIGINAL", "FORM":"F03","LG" : "EN" }).find("SHORT_DESCR", recursive=True)
                description= description.get_text()
                postal_code= soup.find("F03_2014", { "CATEGORY":"ORIGINAL", "FORM":"F03","LG" : "EN" }).find("POSTAL_CODE", recursive=True)
                postal_code= postal_code.get_text()   
                email= soup.find("F03_2014", { "CATEGORY":"ORIGINAL", "FORM":"F03","LG" : "EN" }).find("E_MAIL", recursive=True)
                email= email.get_text()
                amount= soup.find("F03_2014", { "CATEGORY":"ORIGINAL", "FORM":"F03","LG" : "EN" }).find("VAL_TOTAL", recursive=True)
                currency= re.findall(r'"(.*?)"', str(amount))
                amount= amount.get_text()   
                og_notice_no= soup.find("F03_2014", { "CATEGORY":"ORIGINAL", "FORM":"F03","LG" : "EN" }).find("NOTICE_NUMBER_OJ", recursive=True)
                og_notice_no= og_notice_no.get_text()   
                ### Appending Data to Data Frmae
                final_data.at[0,'description']= description
                final_data.at[0,'postal_code']= postal_code
                final_data.at[0,'email']= email
                final_data.at[0,'amount']= amount
                final_data.at[0,'currency']= currency
                final_data.at[0,'og_notice_no']= currency  
            else:
                pass        
        except Exception:
            pass    
            ###### WEB Scrapping For Additional Information #########
            ##### Scrapping Of Tab ######
        try:  
            url='https://ted.europa.eu/udl?uri=TED:NOTICE:{0}:DATA:EN:HTML&src=0&tabId=3'.format(doc_id)        
            response = requests.get(url)    
            html_soup = BeautifulSoup(response.content, 'html.parser')    
            table_data = pd.read_html(response.text) # this parses all the tables in webpages to a list
            table_df = table_data[0]
            # =============================================================================
            # =============================================================================
            table_df.columns =['Symbol','Header','Values']   
            if table_df.empty:
                print("Empty Data Frame")
            else:
                    final_data.at[0,'title']= table_df.loc[table_df['Symbol'] == 'TI','Values'].values
                    final_data.at[0,'notice_publication_number']= table_df.loc[table_df['Symbol'] == 'ND','Values'].values
                    final_data.at[0,'publication_date']= table_df.loc[table_df['Symbol'] == 'PD','Values'].values
                    final_data.at[0,'oj_s__issue_number']= table_df.loc[table_df['Symbol'] == 'OJ','Values'].values
                    final_data.at[0,'town_city_of_the_buyer']= table_df.loc[table_df['Symbol'] == 'TW','Values'].values
                    final_data.at[0,'Official name of the buyer']= table_df.loc[table_df['Symbol'] == 'AU','Values'].values
                    final_data.at[0,'original_language']= table_df.loc[table_df['Symbol'] == 'OL','Values'].values
                    final_data.at[0,'country_of_the_buyer']= table_df.loc[table_df['Symbol'] == 'CY','Values'].values
                    final_data.at[0,'type_of_buyer']= table_df.loc[table_df['Symbol'] == 'AA','Values'].values
                    final_data.at[0,'eu_institution_agency']= table_df.loc[table_df['Symbol'] == 'HA','Values'].values
                    final_data.at[0,'document_sent']= table_df.loc[table_df['Symbol'] == 'DS','Values'].values
                    final_data.at[0,'type_of_contract']= table_df.loc[table_df['Symbol'] == 'NC','Values'].values
                    final_data.at[0,'type_of_procedure']= table_df.loc[table_df['Symbol'] == 'PR','Values'].values
                    final_data.at[0,'notice_type']= table_df.loc[table_df['Symbol'] == 'TD','Values'].values
                    final_data.at[0,'regulation']= table_df.loc[table_df['Symbol'] == 'RP','Values'].values
                    final_data.at[0,'type_of_bid']= table_df.loc[table_df['Symbol'] == 'TY','Values'].values
                    final_data.at[0,'award_criteria']= table_df.loc[table_df['Symbol'] == 'AC','Values'].values
                    final_data.at[0,'common_procurement_vocabulary_(cpv)']= table_df.loc[table_df['Symbol'] == 'PC','Values'].values
                    final_data.at[0,'place_of_performance_(nuts)']= table_df.loc[table_df['Symbol'] == 'RC','Values'].values
                    final_data.at[0,'internet_address_(url)']= table_df.loc[table_df['Symbol'] == 'IA','Values'].values
                    final_data.at[0,'legal_basis']= table_df.loc[table_df['Symbol'] == 'DI','Values'].values
                    final_data.at[0,'deadline_date']= table_df.loc[table_df['Symbol'] == 'DT','Values'].values               
        except Exception:
            pass     
            
            ##### Scraping OF Other Tab  ################             
        try:       
            url='https://ted.europa.eu/udl?uri=TED:NOTICE:{0}:DATA:EN:HTML&src=0&tabId=4'.format(doc_id)       
            response = requests.get(url)       
            html_soup = BeautifulSoup(response.content, 'html.parser')      
            # =============================================================================
          
            # =============================================================================
            anchor_data = html_soup.find_all("a", {"class": "noBg"})     
            past_doc_list=[]
            for values in anchor_data:
                text= values.get_text()
                doc_ids=text[0:text.find(':')]
                past_doc_list.append(doc_ids)
        except Exception:
            pass   
        ### looping and finding past data
        counter=1
        Pub= 'publication_date'
        Dead= 'deadline'
        Doc= 'document'
        Auth= 'authority_Name'   
        try:
            for value in past_doc_list :
                if counter < 100:
                    url='https://ted.europa.eu/udl?uri=TED:NOTICE:{0}:DATA:EN:HTML&src=0&tabId=3'.format(value)
                    response = requests.get(url)
                    past_table = pd.read_html(response.text) # this parses all the tables in webpages to a list
                    past_table = past_table[0] 
                    past_table.columns =['Symbol','Header','Values']
                    key= Doc + '_id_' +str(counter)
                    final_data.at[0,key]=value
                    key= Pub + '_' + str(counter)
                    final_data.at[0,key]=past_table.loc[past_table['Symbol'] == 'PD','Values'].values
                    key= Dead + '_' + str(counter)
                    final_data.at[0,key]= past_table.loc[past_table['Symbol'] == 'DT','Values'].values
                    key= Doc + '_' + str(counter)
                    final_data.at[0,key]= past_table.loc[past_table['Symbol'] == 'TD','Values'].values
                    key= Auth + '_' + str(counter)   
                    final_data.at[0,key]= past_table.loc[past_table['Symbol'] == 'AU','Values'].values
                    counter = counter+1
                else:
                    break
                
        except  Exception:
            pass
        
        
        try:
            latitude,longitude= Geocode.geolocate(country_iso,town)
            final_data.at[0,'latitude']=   latitude
            final_data.at[0,'longitude']=   longitude
    
            
        except Exception:
            pass
        return final_data
    
    
    
