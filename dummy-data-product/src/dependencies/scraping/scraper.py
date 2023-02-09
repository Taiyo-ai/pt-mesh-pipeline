from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd


url = "https://etenders.gov.in/eprocure/app?page=FrontEndTendersByOrganisation&service=page"

class WebScaper(webdriver.Chrome):
    
    def __init__(self,driver_path =r"C:\selenium_drivers\chromedriver_win32"):
        
        super(WebScaper, self).__init__()
        # self.implicitly_wait(10)
        # self.maximize_window()
    
    def send_request(self,url):
        self.get(url)
        
        
        new_html = self.page_source
        # print(new_html)
        get_all_links = self.find_elements(By.CSS_SELECTOR,"a.link2")
        # print(get_all_links)
        total_organization_links = []
        for link in get_all_links:
            total_organization_links.append(link.get_attribute('href'))
            
        # print(total_organization_links)
        total_tender_links = []
        output_data = {
                    'Organisation Chain':[],
                    'Sub Organization':[],
                    'Tender Reference Number': [],
                    'Tender ID':[],
                    'Tender Type':[],
                    'Tender Category':[],
                    'Title':[],
                    'Work Description':[],
                    'Period Of Work(Days)':[],
                    'Bid Submission Start Date':[],
                    'Bid Submission End Date':[],
                    'Bid Opening Date':[],
                    'Name':[],
                    'Address':[],                    
                }
        
        for link in total_organization_links[:1]:
            # print(link)
            self.execute_script(f"window.open('{link}');")
            
            
            # print(self.current_url)
            self.switch_to.window(self.window_handles[1])
            all_links_elements = []
            odd_links = [all_links_elements.append(link) for link in self.find_elements(By.CSS_SELECTOR,'tr.odd')]
            even_links = [all_links_elements.append(link) for link in self.find_elements(By.CSS_SELECTOR,'tr.even')]
            
            all_tender_links = []
            for link in all_links_elements:
                ele = link.find_element(By.TAG_NAME, "a")
                tender_link = ele.get_attribute('href')
                all_tender_links.append(tender_link)
                
            
            for link in all_tender_links[:1]:
                self.execute_script(f"window.open('{link}');")
                # print(self.window_handles)
                self.switch_to.window(self.window_handles[2])
                new_html = self.page_source
                
                soup = BeautifulSoup(new_html, 'html.parser')
                
                titles = soup.find_all("td", class_="td_caption")
                # for title in titles:
                #     print(title.text)
                title_filter = [title for title in titles if title.text in output_data.keys()]
                # values = soup.find_all('td',class_='td_field')
                # print(title_filter)
                titles_text = [title.text for title in title_filter]
                title_values = []
                for title in title_filter:
                    value = title.findNext("td").text
                    title_values.append(value)
                
                
                for title,value in zip(titles_text, title_values):
                    if title == "Organisation Chain":
                        new_title = value.split('||')
                        # print(new_title[0])
                        output_data["Sub Organization"].append(new_title[1])
                        output_data[title].append(new_title[0])
                    else:
                        lis = output_data[title]
                        lis.append(value)
                        
                self.current_window_handle
                self.implicitly_wait(2)
                # print(titles)
                self.close()
                self.switch_to.window(self.window_handles[1])
        
        return output_data
       

    def store_data(self, data):
        
        df = pd.DataFrame(data)
        df.to_excel('output.xlsx', index=True)


def scrape_data():
    """
    main function to call the web scraper
    """
    # options = webdriver.ChromeOptions() 
    # options.add_experimental_option('excludeSwitches', ['enable-logging'])
    # driver = webdriver.Chrome(options=options)
    scraper = WebScaper()
    url = "https://etenders.gov.in/eprocure/app?page=FrontEndTendersByOrganisation&service=page"
    contents = scraper.send_request(url)
    output = scraper.store_data(contents)
    # tender_info = scraper.parse_html(contents)
    # content_new = scraper.parse_html(content)
    # print(content_new)
scrape_data()
    # parsed_content = scraper.parse_data(content)
    # extracted_data = scraper.extract_data(parsed_content)
    # scraper.store_data(extracted_data)
