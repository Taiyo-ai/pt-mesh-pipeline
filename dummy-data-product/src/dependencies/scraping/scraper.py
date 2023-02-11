from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
from dependencies.standardization.standardizer import StandardizeData
from dependencies.cleaning.cleaning import CleanData
import logging

logging.basicConfig(level=logging.INFO)
output_data = []

class WebScaper(webdriver.Chrome):
    
    def __init__(self,driver_path =r"C:\selenium_drivers\chromedriver_win32"):
        
        super(WebScaper, self).__init__()
        # self.implicitly_wait(10)
        # self.maximize_window()
    
    def send_request(self,url):
        """
        Sends request to the url page and returns the total tenders lists
        """
        self.get(url)
        
        #total tender organizations page
        new_html = self.page_source
        
        #links of all organization tenders
        get_all_links = self.find_elements(By.CSS_SELECTOR,"a.link2")
        # print(get_all_links)
        
        logging.info("getting each Organisation links")
        #empty list to store the each organization tenders page
        total_organization_links = []
        for link in get_all_links:
            total_organization_links.append(link.get_attribute('href'))
        
        
        #the required data to extract for
        required_data = [
                    'Organisation Chain',
                    'Tender Reference Number',
                    'Tender Fee in ₹  ',
                    'Tender ID',
                    'Tender Type',
                    'Tender Fee in ₹',
                    'Withdrawal Allowed',
                    'Tender Category',
                    'Product Category',
                    'Tender Value in ₹ ',
                    'Period Of Work(Days)',
                    'Title',
                    'Work Description',
                    'Published Date',
                    'Location',
                    'Bid Submission Start Date',
                    'Bid Submission End Date',
                    'Bid Opening Date',
                    'Bid Validity(Days)',
                    'Name',
                    'Address',                    
        ]
        
        #empty list of data, containing tuple of (title, value) of the tender page
        output_data_list = []
        
        
        #loop through organizations
        for link in total_organization_links[:2]:
            
            
            # print(link)
            #open new window of each individual organization total tenders list
            self.execute_script(f"window.open('{link}');")
            
            #switch to newly created window to get the page source and to do the further process
            self.switch_to.window(self.window_handles[1])
            
            #empty list to append all the tender elements of an organization
            all_links_elements = []
            
            #since all elements does not have proper class, I have taken 'odd' and 'even' class values
            odd_links = [all_links_elements.append(link) for link in self.find_elements(By.CSS_SELECTOR,'tr.odd')]
            even_links = [all_links_elements.append(link) for link in self.find_elements(By.CSS_SELECTOR,'tr.even')]
            
            #empty list to store individual tender links
            all_tender_links = []
            
            
            #loop through the links element list and append all the links
            for link in all_links_elements:
                ele = link.find_element(By.TAG_NAME, "a")
                tender_link = ele.get_attribute('href')
                all_tender_links.append(tender_link)
            
            logging.info(f"scraping data of {len(all_tender_links)} tenders")
            #loop through all tender links
            try:
                for link in all_tender_links[:2]:
                    
                    #open link in new window
                    self.execute_script(f"window.open('{link}');")
                    # print(self.window_handles)
                    
                    #switch to newly created window
                    self.switch_to.window(self.window_handles[2])
                    
                    #get html content of that page
                    new_html = self.page_source
                    
                    soup = BeautifulSoup(new_html, 'html.parser')
                    
                    #find all the elements with the class(i.e Tender ID, Organisation chain, etc)
                    titles = soup.find_all("td", class_="td_caption")
                    
                    #loop through titles and check if the title in required data list
                    title_filter = [title for title in titles if title.text in required_data]
                    
                    #loop through the title filter to get the text(title) of that element
                    titles_text = [title.text for title in title_filter]
                    
                    #empty list to store title values (eg: Airport Authority of India, ..)
                    title_values = []
                    
                    #for each title in the title filter list, get the next element to it coz it is the title value
                    for title in title_filter:
                        value = title.findNext("td").text
                        title_values.append(value)
                    
                    #loop through the 2 list and append title and its value it the output data list
                    #eg: title : Tender Id, value: 233, the append tuple will be ("Tender Id",233)
                    for key, value in zip(titles_text, title_values):
                        output_data_list.append((key,value))
                    
                    
                    self.implicitly_wait(2)
                    
                    #close the current window
                    self.close()
                
                #switch to the previous window(the total tender list of an organization page)
                    self.switch_to.window(self.window_handles[1])
            except Exception as e:
                logging.error(e, exc_info=True)
             
            #close window
            self.close()
            
            #switch to the main page (Total organization list page)
            self.switch_to.window(self.window_handles[0])
            # print(self.window_handles)
        
        return output_data_list
    
    def change_title(self,data):
        """
        Changes the title as it containe multiple names in it.
        
        """
        
        for key,value in data.items():
            if key == 'Organisation Chain':
                title_data = data[key]
                for index,title in enumerate(title_data):
                    
                    title_data.remove(title)
                    split_title = title.split("||")
                    data['Organisation Chain'].insert(index, split_title[0])
                    
        
        return data
                
    
    def clean_scraped_data(self,data):
        """
        cleans the data for the issue with work days
        """
        
        output = CleanData.clean_data(data)
        return output    
      

    def format_data(self,data):
        data_output =  {
                    'Organisation Chain':[],
                    'Tender Reference Number':[],
                    'Tender ID':[],
                    'Tender Type':[],
                    'Withdrawal Allowed':[],
                    'Tender Category':[],
                    'Product Category':[],
                    'Tender Value in ₹ ':[],
                    'Period Of Work(Days)':[],
                    'Title':[],
                    'Work Description':[],
                    'Period Of Work(Days)':[],
                    'Published Date':[],
                    'Location':[],
                    'Bid Submission Start Date':[],
                    'Bid Submission End Date':[],
                    'Bid Opening Date':[],
                    'Bid Validity(Days)':[],
                    'Name':[],
                    'Address':[],                    
                }   
        
        for key,value in data:
            data_output[key].append(value)
        
        return data_output
            
    def standardize_scraped_data(self,data):
        """
        makes titles to snake case
        """
        output = StandardizeData.standardize_data(data)
        data_oupput = StandardizeData.format_date(output)
        return data_oupput
    
    
    def store_data(self, data, mode="csv"):
        
        """
        stores the data in the required mannar
        """
        df = pd.DataFrame(data)
        
        if mode == "xlsx":
            df.to_excel('output.xlsx', index=True)
        else:
            df.to_csv("output.csv", index=True)


def scrape_data():
    """
    main function to call the web scraper
    """
    scraper = WebScaper()
    url = "https://etenders.gov.in/eprocure/app?page=FrontEndTendersByOrganisation&service=page"
    contents = scraper.send_request(url)
    
    logging.info("formating the data ('key': [total values])")
    formated_data = scraper.format_data(contents)
    
    logging.info("Slicing title to get required slice...")
    title_added_data = scraper.change_title(formated_data)
    
    logging.info("Standardizing the data...")
    standard_data = scraper.standardize_scraped_data(title_added_data)
    
    logging.info("Cleaning the output...")
    cleaned_output = scraper.clean_scraped_data(standard_data)
    # print(cleaned_output)
    
    logging.info('Storing the data...')
    scraper.store_data(cleaned_output,mode="xlsx")
    
    
    logging.info("successfully done scraping.")
    # print(standard_data)
    # print(contents)
    # standard_data = scraper.standardize_data(contents)
    # print(standard_data)
    # output = scraper.store_data(contents)
  
scrape_data()
   


