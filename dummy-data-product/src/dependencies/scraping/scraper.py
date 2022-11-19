from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas as pd
import zipfile
import ssl
import json
import csv

with open("cpv.html", encoding="utf-8") as openfile:
    data = openfile.read()
    soup = BeautifulSoup(data, 'html5lib')
    id=[]
    sector=[]
    for element in soup.find_all("a", {"class": "cpv-click"}):
        id.append(element['data-cpv'])
        sector.append(element['data-cpv-des'])
cpv_map= dict(zip(id,sector))


def scrape(site):
    class data:
        def __init__(self):
            self.name = ""
            self.description = ""
            self.source=""
            self.status=""
            self.identified_status="" 
            self.project_or_tender=""
            self.budget= ""
            self.url= ""
            self.document_urls= ""
            self.sector= ""
            self.subsector= ""
            self.identified_sector= ""
            self.identified_subsector= ""
            self.identified_sector_subsector_tuple= ""
            self.entities= ""
            self.country_name= ""
            self.country_code= ""
            self.region_name= ""
            self.region_code= ""
            self.state= ""
            self.locality= ""
            self.neighbourhood= "" 
            self.location= ""
            self.map_coordinates=""
            self.timestamps= ""            
            self.timestamp_range= ""
            self.timestamp_range_2= ""

    if site=='EU':
        with open('pt-mesh-pipeline\dummy-data-product\src\dependencies\scraping\example.json', 'r') as openfile:
            object = json.load(openfile)
            for row in object:
                scraped_data.name=object['releases'][row]['buyer']['name']
                scraped_data.description= object['releases'][row]['tender']['awardCriteriaDetails']
                scraped_data.identified_status= "Stage 3"
                scraped_data.project_or_tender=object['releases'][row]['initiationType']
                scraped_data.budget= object['releases'][row]['awards'][0]['value']['amount']
                scraped_data.url= object['uri']
                scraped_data.document_urls= object['releases'][row]['awards'][0]['documents'][0]['url']
                scraped_data.sector= object['releases'][row]['tender']['mainProcurementCategory']
                scraped_data.country_name= object['releases'][row]['parties'][0]['address']['countryName']
                scraped_data.region_code= object['releases'][row]['parties'][0]['address']['postalCode']
                scraped_data.neighbourhood= object['releases'][row]['parties'][0]['address']['streetAddress']
                scraped_data.timestamps= object['releases'][row]['awards'][0]['documents'][0]['datePublished']
                scraped_data.timestamp_range= object['releases'][row]['awards'][0]['date']
                scraped_data.timestamp_range_2= object['releases'][row]['date'] 
                raw_data = json.dumps(scraped_data.__dict__)
        return raw_data

    if site=='USGOV':
        
        zf = zipfile.ZipFile('C:/Users/Rajini/Desktop/Coding/jobs/pt-mesh-pipeline/data-ted-csv.zip')
        df=pd.read_csv('USGOV.csv')
        object= df.to_numpy()
        for row in object:
            scraped_data=data
            scraped_data.name=names.name
            scraped_data.description= 
            scraped_data.source=
            scraped_data.status= 
            scraped_data.identified_status= 
            scraped_data.project_or_tender=
            scraped_data.budget= 
            scraped_data.url= 
            scraped_data.document_urls=
            scraped_data.sector= 
            scraped_data.subsector
            scraped_data.identified_sector
            scraped_data.identified_subsector
            scraped_data.identified_sector_subsector_tuple
            scraped_data.entities
            scraped_data.country_name= 
            scraped_data.country_code
            scraped_data.region_name
            scraped_data.region_code=
            scraped_data.state
            scraped_data.locality
            scraped_data.neighbourhood= 
            scraped_data.location
            scraped_data.map_coordinates
            scraped_data.timestamps= 
            scraped_data.timestamp_range= 
            scraped_data.timestamp_range_2= 
            raw_data_2 = json.dumps(scraped_data.__dict__)
        return raw_data_2

    if site=='FL':
        df=pd.read_csv('Florida.csv')
        object= df.to_numpy()
        scraped_data=data
        for row in object:
            scraped_data.name=object[row][1]
            scraped_data.description=object[row][4] 
            scraped_data.project_or_tender='tender'
            scraped_data.budget= object[row][11]
            scraped_data.source= 'Florida Procurement'
            scraped_data.url= 'https://pdaexternal.fdot.gov/Pub/AdvertisementPublic/AllAdDetail/PS/A'
            scraped_data.document_urls= 'https://pdaexternal.fdot.gov/Pub/AdvertisementPublic/AllAdDetail/PS/A#'
            scraped_data.sector=object[row][7]
            scraped_data.subsector=object[row][8]
            scraped_data.country_name='USA'
            scraped_data.region_name= 'District' +' '+ object[row][8] + ', Florida'
            scraped_data.state='Florida'
            scraped_data.locality= 'See Region Name'
            scraped_data.neighbourhood= [row][4]
            scraped_data.timestamps= [row][11]
            scraped_data.timestamp_range= [row][11]
            scraped_data.timestamp_range_2= [row][14] 
            raw_data_3 = json.dumps(scraped_data.__dict__)
        return raw_data_3

    if site=='TX':
        df=pd.read_csv('Texas.csv')
        object= df.to_numpy()
        scraped_data= new data()
        with open('pt-mesh-pipeline\dummy-data-product\src\dependencies\scraping\Texas.json', 'r') as openfile:
            object_2 = json.load(openfile)
            for row in object_2['features'][row]:
                scraped_data.budget= object_2['features'][row]['properties']['EST_CONST_COST']

            for row in object:
                scraped_data.name=object[row][0]
                scraped_data.description=object[row][9] + [row][10]
                scraped_data.status=object[row][32]
                scraped_data.source= 'Texas Procurement'
                scraped_data.project_or_tender= 'Project'
                scraped_data.url= 'https://www.txdot.gov/projects/project-tracker.html'
                scraped_data.document_urls= 'https://gis-txdot.opendata.arcgis.com/datasets/TXDOT::txdot-dcis-all-projects/explore'
                scraped_data.sector= object[row][6]                         
                scraped_data.subsector= object[row][9]
                scraped_data.country_name= 'USA'
                scraped_data.region_name= object[row][24]
                scraped_data.state='Texas'
                scraped_data.region_code= object[row][3]
                scraped_data.locality= object[row][25]
                scraped_data.neighbourhood= object[row][7] + object[row][8]
                scraped_data.timestamps= object[row][15]
                scraped_data.timestamp_range= object[row][15]
                scraped_data.timestamp_range_2= object[row][27] 
                raw_data_4 = json.dumps(scraped_data.__dict__)
        return raw_data_4


    if site== 'CA':
        df=pd.read_csv('Cali.csv')
        object= df.to_numpy()
        for row in object:
            scraped_data.name=object[row][0]
            scraped_data.description=object[row][3]
            scraped_data.source= 'California Procurement'
            scraped_data.status= 'Closed'
            scraped_data.identified_status='Stage 3' 
            scraped_data.project_or_tender='tender'
            scraped_data.budget= 'N/A'
            scraped_data.url= 'https://dot.ca.gov/programs/procurement-and-contracts/contracts-out-for-bid'
            scraped_data.document_urls= 'https://caleprocure.ca.gov/pages/Events-BS3/event-search.aspx' 
            scraped_data.sector=[row][1] 
            scraped_data.subsector= [row][3]
            scraped_data.country_name='USA' 
            scraped_data.region_name='N/A'
            scraped_data.region_code='N/A'
            scraped_data.state='Cali'
            scraped_data.locality='N/A'
            scraped_data.neighbourhood='N/A'
            scraped_data.location='N/A'
            scraped_data.map_coordinates='N/A'
            scraped_data.timestamps=object[row][3] 
            scraped_data.timestamp_range=object[row][3] 
            scraped_data.timestamp_range_2=object[row][3]    
            raw_data_5 = json.dumps(scraped_data.__dict__)
        return raw_data_5

    if site=='UK':
        df=pd.read_csv('UK.csv')
        object= df.to_numpy()
        scraped_data.name=object[row][5]
        scraped_data.description=object[row][6]
        scraped_data.source=[row][2]
        scraped_data.status=object[row][3]
        scraped_data.project_or_tender='tender' if object[row][1]=='Contract' else 'Undefined'
        scraped_data.budget= object[row][35] if object[row][35].isnan==False and object[row][35]!=0 else object[row][33] if object[row][33].isnan==False and object[row][33]!=0 else object[row][32]
        scraped_data.url= object[row][19]
        scraped_data.document_urls= object[row][21]
        scraped_data.sector= object[row][31]
        for key, value in cpv_map.items():
            if str(key)[:2]==str(object[0][10][:2]):                          
                scraped_data.subsector=str(value)    
        scraped_data.subsector= next(iter(d.items())) 
        scraped_data.country_name= object[row][17]
        scraped_data.region_name= object[row][9]
        scraped_data.region_code= object[row][16]
        scraped_data.locality= object[row][15]
        scraped_data.neighbourhood= object[row][13]+' ,'+object[row][14]
        scraped_data.timestamps= object[row][23]
        scraped_data.timestamp_range= object[row][23]
        scraped_data.timestamp_range_2= object[row][24] 
        raw_data_6 = json.dumps(scraped_data.__dict__)
        return raw_data_6


