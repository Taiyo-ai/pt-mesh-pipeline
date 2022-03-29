

class Scraper():
    def __init__(self):
        self.url = "https://www.contractsfinder.service.gov.uk/Search/Results?&page=1"
    

    def getMetadata(self):
        """ This method will scrape the metadata from the website """
        import metadata_parser
        import json
        try:
            page= metadata_parser.MetadataParser(self.url)
            dictionary = page.metadata
            with open("../../data/metadata.json", "w") as outfile:
                json.dump(dictionary, outfile,indent=4)
            print("Metadata successfully scraped")

        except Exception as e:
            print("Error in metadata".e)
    
    def getScrapedData(self)->list:
        """ This method will scrape the data from the website """
        import requests
        from bs4 import BeautifulSoup 

        try:
            response=requests.get(self.url )
            if response.status_code !=200:
                raise "Not able to connect to the server"

           
            soup =BeautifulSoup(response.text,'lxml')
            search = soup.find_all("div",class_="search-result")
            scraped_data = []

            for f in search:
                s = f.text
                s = s.replace("\n\n","")
                s = s.replace("\n\xa0\n", "+")
                s = s.replace("\r\n\r\n","+")
                scraped_data.append(s)

            return scraped_data
        except Exception as e:
            print("Error in data scrapping",e)

    def doCleanup(self ,scraped_data):
        """ This method will clean the data """

        bid_title = []
        contract_location = []
        procurement = []
        notice_status = []
        closing_date = []
        contract_value = []
        location =[]
        pub_date = []

        try:
            for i in range(len(scraped_data)):
                data = scraped_data[i].strip().replace("\n","+").split("+")
                data = "+".join(data).lower()

                # Handling null values
                if "procurement stage" not in data:
                    procurement.append("Not Available")

                if "notice status" not in data:
                    notice_status.append("Not Available")
                
                if "contract location" not in data:
                    location.append("Not Available")

                if "contract value" not in data:
                    contract_value.append("Not Available")

                if "publication date" not in data:
                    pub_date.append("Not Available")

                else:
                    data = data.split("+")
                    for i in range(len(data)):
                        if i==0:
                            bid_title.append(data[i])
                        if i==1:
                            contract_location.append(data[i])

                        if "procurement stage" in data[i]:
                            proc = data[i].split("procurement stage")
                            proc = " ".join(proc)
                            procurement.append(proc)

                        if "notice status" in data[i]:
                            proc = data[i].split("notice status")
                            proc = " ".join(proc)
                            notice_status.append(proc)

                        if "approach to market date" in data[i]:
                            proc = data[i].split("approach to market date ")
                            proc = " ".join(proc)
                            closing_date.append(proc)

                        if "closing" in data[i]:
                            proc = data[i].split("closing ")
                            proc = " ".join(proc)
                            closing_date.append(proc)

                        if "contract location" in data[i]:
                            proc = data[i].split("contract location ")
                            proc = " ".join(proc)
                            location.append(proc)   

                        
                        if "contract value" in data[i]:
                            proc = data[i].split("contract value ")
                            proc = " ".join(proc)
                            contract_value.append(proc)

                        if "publication date" in data[i]:
                            proc = data[i].split("publication date ")
                            proc = " ".join(proc)
                            proc = proc.split(",")
                            proc = " ".join(proc[0].split())
                            pub_date.append(proc)

            print("Data has successfully been cleaned")
            features= dict(bid_title=bid_title,contract_location=contract_location,\
                           procurement=procurement,notice_status=notice_status,closing_date=closing_date,\
                           contract_value=contract_value,location=location,pub_date=pub_date)
            return features

        except Exception as e:
            print("Error in data cleaning",e)

    def generateCSV(self,features):
        """ This method will generate the csv file """
        import pandas as pd

        try:
            df =pd.DataFrame(features)
            df.to_csv("../../data/data.csv",index=False)
            print("CSV file successfully generated")
        except Exception as e:
            print("Error in generating CSV file",e)
