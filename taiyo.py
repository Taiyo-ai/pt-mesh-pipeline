#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from time import sleep
from numpy import tensordot
from selenium.common.exceptions import *
from click import NoSuchOption
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd


final_data=pd.DataFrame() #Initiating Dataframe to store data
tender_name_list=[]#Initiating List to store respective tender name
Industry_list=[]#Initiating List to store respective industry
Location_of_contract_list=[]#Initiating List to store respective location of contract
Value_of_contract_list=[]#Initiating List to store respective value of contract
Procurement_reference_list=[]#Initiating List to store respective procurment 
Published_date_list=[]#Initiating List to store respective published date
Closing_date_list=[]#Initiating List to store respective closing date
Closing_time_list=[]#Initiating List to store respective clossing time

chrome_options = Options()
chrome_options.add_argument('--disable-notifications')
chrome_options.add_argument('--disable-popup-blocking')
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path="C:/Users/Admin/AppData/Local/Temp/Rar$EX00.172/chromedriver.exe",options=chrome_options) #La unching Chrome Driver
for z in range(1,7):  #Note-Increase the range and we can scrape more data
    try:
        driver.get(f'https://www.contractsfinder.service.gov.uk/Search/Results?page={z}#07c879eb-5e62-435b-8034-10e114ec9938')
        sleep(2) 
        
        for x in range(1,21):
                try:
                    driver.find_element(By.XPATH,f'//div[3]/div/div/div/div[1]/div[{x}]/div[1]/h2/a').click()
                    sleep(2)
                    try:
                        tender_name=driver.find_element(By.XPATH,'//h1[@class="govuk-heading-l break-word"]')
                        tender_name_list.append(tender_name.text)
                    except:
                        tender_name_list.append('tender name missing')

                    try:
                        industry=driver.find_element(By.XPATH,'//*[@id="content-holder-left"]/div[3]/ul/li/p')
                        Industry_list.append(industry.text)
                    except:
                        Industry_list.append('industry missing')

                    try:    
                        location_of_contract=driver.find_element(By.XPATH,'//*[@id="content-holder-left"]/div[3]/p[2]/span')
                        Location_of_contract_list.append(location_of_contract.text)
                    except:
                        Location_of_contract_list.append('location of contract missing')
                    
                    try:
                        value_of_contract=driver.find_element(By.XPATH,'//*[@id="content-holder-left"]/div[3]/p[3]')
                        Value_of_contract_list.append(value_of_contract.text)
                    except:
                        Value_of_contract_list.append('value of contract missing')

                    try:
                        procurement_reference=driver.find_element(By.XPATH,'//*[@id="content-holder-left"]/div[3]/p[4]')
                        Procurement_reference_list.append(procurement_reference.text)
                    except:
                        Procurement_reference_list.append('procurement reference missing')

                    try:
                        published_date=driver.find_element(By.XPATH,'//*[@id="content-holder-left"]/div[3]/p[5]')
                        Published_date_list.append(published_date.text)
                    except:
                        Published_date_list.append('published date missing')

                    try:
                        closing_date=driver.find_element(By.XPATH,'//*[@id="content-holder-left"]/div[3]/p[6]')
                        Closing_date_list.append(closing_date.text)
                    except:
                        Closing_date_list.append('closing date missing')
                    
                    try:
                        closing_time=driver.find_element(By.XPATH,'//*[@id="content-holder-left"]/div[3]/p[7]')
                        Closing_time_list.append(closing_time.text)
                    except:
                        Closing_time_list.append('closing time missing')

                        
                except:
                    print('NO DATA RECEIVED')
                driver.back()
                
    except:
        print('INVALID URL')


final_data['Tender name']=tender_name_list
final_data['Industry']=Industry_list
final_data['Location of contract']=Location_of_contract_list
final_data['Value of contract']=Value_of_contract_list
final_data['Procurment references']=Procurement_reference_list
final_data['Published date']=Published_date_list
final_data['closing date']=Closing_date_list
final_data['closing time']=Closing_time_list
final_data.to_csv('C:\Users\Admin\Desktop\tender_project.csv')


# In[ ]:




