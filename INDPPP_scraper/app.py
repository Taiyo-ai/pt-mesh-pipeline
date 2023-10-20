import os
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen, Request
import csv
import spacy
import logging
import string
from datetime import datetime
import time
import pgeocode
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
# Download NLTK and spacy data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('averaged_perceptron_tagger')




def get_all_links(url, session_token):
    try:
        logging.info('get_all_links started successfully')
        try:
            request1 = Request(url, headers={'Cookie': f'JSESSIONID={session_token}'})
            # Opening the URL with the custom request using urlopen
            urlclient = urlopen(request1)
            cppp_page = urlclient.read() #reading the html page
            soup = bs(cppp_page, "lxml") #creating the soup

            time.sleep(3)

            article_find = soup.find_all(class_ = 'link2')
            for link_element in article_find:
                link_href = link_element.get('href')
                link_list.add(link_href)
        except Exception as e:
            logging.info(f"Error in accessing url: {e}")

        try:

            for i in link_list:
                link = 'https://etenders.gov.in'+ i
                request2 = Request(link, headers={'Cookie': f'JSESSIONID={session_token}'})

                linkclient = urlopen(request2)
                tender_page = linkclient.read() #reading the html page
                soup2 = bs(tender_page, "lxml")
                tender_elements = soup2.find_all('a', {'title': 'View Tender Information'})
                
                # Extracting the href attribute values from all matching elements
                for j in tender_elements:
                    tender_links = j.get('href')
                    tender_link.add(tender_links)
                time.sleep(5)
        except Exception as e:
            logging.info(f"An error occurred while accessing link: {link}, {e}")
        logging.info("get_all_links ended successfully")
    except Exception as e:
        logging.info(f"An error occured in get_all_links: {e}")


def scraping_page(session_token):
    try:
        logging.info("Scraping_page started successfully")
        for k in tender_link:
            try:
                logging.info("Iteration of tender_link started successfully")
                link2 = 'https://etenders.gov.in'+ k
                print(link2)
                request2 = Request(link2, headers={'Cookie': f'JSESSIONID={session_token}'})

                link2client = urlopen(request2)
                tender_details = link2client.read() #reading the html page
                soup3 = bs(tender_details, "lxml")
            except Exception as e:
                logging.info(f"An error occured in link2: {link2}, {e}")

            try:
                td_caption_elements = soup3.find_all('td', class_='td_caption')

                #For original id
                # Iterating through the <td> elements for finding the "Tender ID" label
                for td in td_caption_elements:
                    if "Tender ID" in td.get_text():
                        # Extracting the text from the next <td> element
                        original_id = td.find_next('td').get_text(strip=True)
            except:
                original_id = "NaN"
            try:
                title = soup3.find('td', class_='td_caption', string='Title').find_next('td').get_text(strip=True)
            except:
                title = "NaN"
            try:

                work_description = soup3.find('td', class_='td_caption', string='Work Description').find_next('td').get_text(strip=True)
            except:
                work_description = "NaN"
            try:    
                tender_value = soup3.find('td', class_='td_caption', string='Tender Value in ₹ ').find_next('td').get_text(strip=True)
                if tender_value != 'NA':
                    budget = float(tender_value.replace(',', '')) // 83.15
                else:
                    budget = tender_value
            except:
                budget = "NaN"   
            try:     
                product_category = soup3.find('td', class_='td_caption', string='Product Category').find_next('td').get_text(strip=True)
            except:
                product_category = "NaN"
            try:    
                subcategory = soup3.find('td', class_='td_caption', string='Sub category').find_next('td').get_text(strip=True)
            except:
                subcategory = "NaN"
            try:
                contract_type = soup3.find('td', class_='td_caption', string='Contract Type').find_next('td').get_text(strip=True)
                if contract_type == 'Tender':
                    P_or_T = "T"
                else:
                    P_or_T = "P"
            except:
                contract_type = "NaN"    
                
            try:    
                location = soup3.find('td', class_='td_caption', string='Location').find_next('td').get_text(strip=True)
            except:
                location = "NaN"
            try:    
                pincode = soup3.find('td', class_='td_caption', string='Pincode').find_next('td').get_text(strip=True)
            except:
                pincode = "NaN"

            address = f"{location, }"+f"{pincode}"
            country_code = 'IN'
            nomi = pgeocode.Nominatim(country_code)
            
            # Performing geocoding
            location_info = nomi.query_postal_code(pincode)


            if not location_info.empty:
                coordinates = (location_info['latitude'], location_info['longitude'])
                state = location_info['state_name']
                county = location_info['county_name']
                locality = location_info['place_name']
                neighbourhood = location_info['community_name']
            else:
                coordinates = "NaN"
                state = "NaN"
                county = "NaN"
                locality = "NaN"
                neighbourhood = "NaN"
            
                    
            try:        
                tables = soup3.find_all('table', {'class': 'tablebg'})
                target_table = None

                for table in tables:
                    if 'Published Date' in table.get_text():
                        target_table = table
                        break

                if target_table:
                    # Finding all <td> elements within the target table
                    td_elements = target_table.find_all('td')

                    # Create a dictionary to store the date values
                    date_dict = {}
                    current_caption = None

                    for td_element in td_elements:
                        # Check if the <td> contains a <b> tag
                        bold_tag = td_element.find('b')
                        if bold_tag:
                            # This is a caption
                            current_caption = bold_tag.get_text(strip=True)
                        else:
                            # This is a date, use the last valid caption
                            if current_caption:
                                date = td_element.get_text(strip=True)
                                if date != 'NA':
                                    date1 = datetime.strptime(date, '%d-%b-%Y %I:%M %p')
                                    # Formatting the date as required YYYY-MM-DD HH:MM:SS
                                    formatted_date = date1.strftime('%Y-%m-%d %H:%M:%S')
                                    date_dict[current_caption.lower()] = formatted_date
                                else:
                                    date_dict[current_caption.lower()] = date
                    time_stamps = date_dict
            except:
                time_stamps = {}
            try:    
                min_date = date_dict.get('document download / sale start date', 'NA')
                max_date = date_dict.get('document download / sale end date', 'NA')
                timestamp_range = {'min': min_date, 'max': max_date}
            except:
                timestamp_range = {}


            try:
                document_urls = []

                anchor_tag = soup3.find('a', {'id': 'docDownoad'})
                if anchor_tag:
                    href_link1 = anchor_tag.get('href')
                    document_urls.append('https://etenders.gov.in'+href_link1)

                # Finding all the links with class "blue_link"
                blue_links = soup3.find_all('a', class_='blue_link')

                # Extracting the href attributes of these links
                for link in blue_links:
                    href_link2 = link.get('href')
                    document_urls.append('https://etenders.gov.in'+href_link2)
            except:
                document_urls = []

            try:
                PPP_text = f"{title} "+f"{work_description}"

                PPP_text = PPP_text.translate(str.maketrans('', '', string.punctuation))

                # Tokenizing the text into words
                words = word_tokenize(PPP_text)

                # Filter out stopwords
                filtered_words = [word for word in words if word.lower() not in stopwords.words('english')]
                fdist = FreqDist(filtered_words)

                # Getting the most common words as keywords
                keywords = [keyword for keyword, count in fdist.most_common(10)]
            except:
                keywords = ["NaN"]

            try:
                # Loading the spaCy model
                nlp = spacy.load("en_core_web_sm")

                # Processing  text
                doc = nlp(PPP_text)

                # Extracting named entities
                named_entities = [ent.text for ent in doc.ents]
            except:
                named_entities = ["NaN"]
    


            
            data_format = {"aug_id":f"IndiaPPP_{original_id}",
                    "original_id": original_id,
                    "project_or_tender": P_or_T,
                    "name": title,
                    "description": work_description,
                    "source":"IndiaPPP",
                    "status": "Proposed",
                    "identified_status": "Proposed",
                    "budget": budget ,
                    "url": link2 ,
                    "document_urls": document_urls,
                    "sector": product_category,
                    "subsector": subcategory,
                    "identified_sector": product_category,
                    "identified_subsector":subcategory,
                    "identified_sector_subsector_tuple":(product_category,subcategory),
                    "keywords":keywords,
                    "entities":named_entities,
                    "country_name":"India",
                    "country_code":"IND",
                    "region_name":"South Asia",
                    "region_code":"SAS",
                    "state":state,
                    "county":county,
                    "locality":locality,
                    "neighbourhood":neighbourhood,
                    "location":address,
                    "map_coordinates":coordinates,
                    "timestamps":time_stamps,
                    "timestamp_range":timestamp_range,
                    }
            # Appending the data to the data_list
            data_list.append(data_format)
            print(data_format)
            logging.info("Scraping_page was successfull")
            time.sleep(5)
    except Exception as e:
        logging.info(f"Exception occured in scraping_page: {e}")


def saving_data(csv_file_path, url, session_token):
    try:
        logging.info("saving_data started")
        get_all_links(url, session_token)
        scraping_page(session_token)

        with open(csv_file_path, mode='w', newline='',encoding='utf-8-sig') as csv_file:
            fieldnames = [
                        "aug_id", "original_id", "project_or_tender", "name", "description", "source", "status", "identified_status", "budget",
                        "url", "document_urls", "sector", "subsector", "identified_sector", "identified_subsector",
                        "identified_sector_subsector_tuple", "keywords", "entities", "country_name", "country_code",
                        "region_name", "region_code", "state", "county", "locality", "neighbourhood", "location",
                        "map_coordinates", "timestamps", "timestamp_range"]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            # Writing the header row
            writer.writeheader()

            # Writing the data rows
            for data in data_list:
                writer.writerow(data)
        logging.info(f"saving_data successful. File_name:{csv_file_path}")       
    except Exception as e:
        logging.info("Exception occured in saving_data", e)






#for logging        
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log" 
logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE)
os.makedirs(logs_path, exist_ok=True)
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)
logging.basicConfig(
            filename=LOG_FILE_PATH,
            format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
            level=logging.INFO)

link_list = set()
tender_link = set()
data_list = []
session_token = input("Enter the JSESSIONID") # check instruction.pdf for reference
url = 'https://etenders.gov.in/eprocure/app?page=FrontEndTendersByOrganisation&service=page'
csv_file_name = 'PPP_tenders2.csv'
csv_file_path = os.path.join(os.getcwd(), csv_file_name)
saving_data(csv_file_path, url, session_token)