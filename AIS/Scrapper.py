import re
import requests 
import pymongo
import json
from datetime import datetime
from bs4 import BeautifulSoup
from threading import Thread

# Url For The Website need to be scraped
url = "https://www.aishub.net/stations?page="

#Converting Scraped data content into bs4
bs4_data = BeautifulSoup(requests.get(url).content,'lxml') 

# creating class
class vessel_status:
    def __init__(self,source):
        self.data = {"ids":{}} #dictionary to store extracted data
        self.table = source.find('table', attrs={'class':"table dataTable table-bordered table-condensed table-striped table-hover kv-grid-table"}) ##find table of station details from web 
        self.ids = list(t.getText() for t in self.table.findAll('td', attrs={"data-col-seq":"0"})) #extracting all The station id for recursive approch

    def scrape_data(self,length=0):
        """ Scraping data from the table of stations details 
        Station id, Country, location, available ships and distinct ships.
        """
        if length == len(list(t.text for t in self.table.findAll('td', attrs={"data-col-seq":"0"}))):
            return self.data
        else:
            # key data
            f = self.table.find('tr', attrs={'data-key':f'{self.ids[length]}'})
            self.data['ids'][f'{self.ids[length]}'] = {}
            H = list(head.getText() for head in self.table.findAll('th'))
            for i in range(1, 7):
                d = f.find('td', attrs={"data-col-seq":f"{i}"}).getText()
                if d is '':
                    pass
                elif '%' in d:
                    pass
                else:
                    if '\xa0' in d:
                        self.data['ids'][f'{self.ids[length]}'][f"{H[i]}"] = d.replace('\xa0','').strip()
                    else:
                        self.data['ids'][f'{self.ids[length]}'][f"{H[i]}"] = d
            #extract link for vessel data
            link = f.find('a', attrs={'href': re.compile("^https://")})
            if self.data['ids'][f'{self.ids[length]}']["Ships"] == '0':
                self.data['ids'][f'{self.ids[length]}']['Vessels'] = None
            else:
                self.data['ids'][f'{self.ids[length]}']['Vessels'] = {"Status_URL":f"{link.get('href')}"+"?page=","MMSI":{}}
            self.data['ids'][f'{self.ids[length]}']['Updated_Time'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            return self.scrape_data(length+1)
            
    def vessel_data_scrap(self,url,id,length=1):
        """
            Extracting Details of vessels avaliable online location and id specified. 
        """
        page = BeautifulSoup(requests.get(url+str(length)).content,'lxml')
        if length == (int(int(page.find('div', attrs={ 'class' : 'summary'}).findAll('b')[1].getText())/8)+1):
            return self.data
        else:
            for r in range(len(page.findChild('tbody').findAll('tr'))):
                td = list(tsd.getText() for tsd in page.findChild('tbody').findAll('tr')[r].findAll('td'))
                for i in range(len(td)):
                    if i == 0:
                        self.data['ids'][f'{id}']['Vessels']['MMSI'][f'{td[0]}'] = {}
                    elif i == 1:
                        self.data['ids'][f'{id}']['Vessels']['MMSI'][f'{td[0]}']['Name'] = td[i]
                    elif i == 2:
                        self.data['ids'][f'{id}']['Vessels']['MMSI'][f'{td[0]}']['Distinct'] = td[i]
                    elif i == 3:
                        self.data['ids'][f'{id}']['Vessels']['MMSI'][f'{td[0]}']['Last_Updates'] = td[i]
                    else:
                        pass
            return self.vessel_data_scrap(url,id,length + 1)

    def Load_ALL_Vessel_Data(self,length=0):
        """
        loading the vessels data in data dictonary with recursion for faster extraction
        """
        if length == len(self.ids):
            return self.data
        else:
            if self.data['ids'][f'{self.ids[length]}']['Vessels'] == None:
                pass
            else: 
                url = self.data['ids'][f'{self.ids[length]}']['Vessels']['Status_URL']
                self.vessel_data_scrap(url, self.ids[length])
            return self.Load_ALL_Vessel_Data(length+1)

    def load_config(self,save_on_local_system=False,Local_Path='',Save_on_Mongodb_db=False,db_URL='',Collection_name="Scraped_Data"):
        """ 
        This fuction is used to specify the save destination of scraped data
        TO save data on local system:
            load_config(save_on_local_system=True,Local_Path="{Your path to save data}")
        TO save data on Mongodb database:
            load_config(Save_on_Mongodb_db=True,db_URL="{Database connection url}",Collection_name="{Collection name you want to use inside mongodb db(by default it use Scraped_Data as collection name)}")
        """
        if save_on_local_system:
            with open(Local_Path+'Submission.json','w') as output_file: ## Load (can be done over database(MongoDB, Mysql, etc) but for now just save in local file called submission.json )
                output_file.write( json.dumps(self.data, indent=4))
        elif Save_on_Mongodb_db:
            myclient = pymongo.MongoClient(db_URL)
            mydb = myclient["AIS_Database"]
            mycol = mydb[Collection_name]
            mycol.insert_one(self.data)
        else:
            return "Please select any save option"

    def run(self):
        self.scrape_data() ## Extract
        self.Load_ALL_Vessel_Data() ## Transform
        self.load_config(save_on_local_system=True,Local_Path="") ## Load (can be done over database(MongoDB, Mysql, etc) but for now just save in local file called submission.json )
        #self.load_config(Save_on_Mongodb_db=True,db_URL="mongodb://127.0.0.1:27017/")   

if __name__ == '__main__':
    ETL = vessel_status(bs4_data)
    ETL.run()
    print(ETL.data)



