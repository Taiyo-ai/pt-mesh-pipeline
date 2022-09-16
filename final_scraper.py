from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
import pandas as pd

driver = webdriver.Chrome(executable_path="C:/drivers/chromedriver8.exe") # Needed to be editied according to requirement

class Scraper:

    def opentender_scrape(self):
        list_buyer = []
        list_tender_link = []
        list_supplier = []
        list_bid_price = []
        url = 'https://opentender.eu/all/search/tender'
        driver.get(url)
        sleep(7)
        while True:
            td_xpath = '//td[@_ngcontent-c17]'
            ele = driver.find_elements(By.XPATH, td_xpath)
            count = 2
            while count < len(ele):
                list_buyer.append(ele[count].text)
                count += 5
            count = 3
            while count < len(ele):
                list_supplier.append(ele[count].text)
                count += 5
            count = 4
            while count < len(ele):
                list_bid_price.append(ele[count].text)
                count += 5
            link_xpath = '//a[@title="Profile Page undefined"]'
            ele = driver.find_elements(By.XPATH, link_xpath)
            for x in ele:
                list_tender_link.append(x.get_attribute('href'))
            try:
                next_xpath = '//button[@class="page-btn page-next"]'
                next_button = driver.find_element(By.XPATH, next_xpath)
                driver.execute_script("arguments[0].click();", next_button)
            except:
                break
        try:
            data = pd.DataFrame()
            data['Buyer'] = list_buyer
            data['Supplier'] = list_supplier
            data['Tender Lnk'] = list_tender_link
            data['Bid Price'] = list_bid_price
            data.to_csv('Opentender_Scraped_data.csv')
            print('CSV File Created successfully')
        except:
            print('Error in Creating CSV File')

    def samgov_scraper(self):
        list_name = []
        list_status = []
        list_physical_address = []
        list_classification = []
        list_activation = []
        list_deactivation = []
        list_unique_id = []
        list_cage_code = []
        url = 'https://sam.gov/search/?page=1&pageSize=25&sort=-modifiedDate&sfm%5BsimpleSearch%5D%5BkeywordRadio%5D=ALL'
        driver.get(url)
        sleep(6)
        pop_up_xpath = '//usa-icon[@class="ng-tns-c72-1"]'
        pop_up = driver.find_element(By.XPATH, pop_up_xpath)
        driver.execute_script("arguments[0].click();", pop_up)
        sleep(5)
        checkbox_xpath = '//input[@class="usa-checkbox__input"]'
        active_checkbox = driver.find_element(By.XPATH, checkbox_xpath)
        driver.execute_script("arguments[0].click();", active_checkbox)
        sleep(7)
        main_count = 0
        while main_count<10:
            main_count+=1
            name_xpath = '//a[@class="usa-link"]'
            ele = driver.find_elements(By.XPATH, name_xpath)
            count = 1
            while count < len(ele):
                list_name.append(ele[count].get_attribute('text'))
                count += 1
            status_xpath = '//span[@class="sds-tag status-tag"]'
            ele = driver.find_elements(By.XPATH, status_xpath)
            for x in ele:
                list_status.append(x.text)
            address_xpath = '//div[@class="sds-static margin-top-2px ng-star-inserted"]'
            ele = driver.find_elements(By.XPATH, address_xpath)
            for x in ele:
                list_physical_address.append(x.text)
            class_xpath = '//div[@class="sds-static"]'
            ele = driver.find_elements(By.XPATH, class_xpath)
            count = 0
            while count < len(ele):
                list_classification.append(ele[count].text)
                count += 3
            count = 1
            while count < len(ele):
                list_activation.append(ele[count].text)
                count += 3
            count = 2
            while count < len(ele):
                list_deactivation.append(ele[count].text)
                count += 3
            id_xpath = '//div[@class="sds-static margin-top-1"]'
            ele = driver.find_elements(By.XPATH, id_xpath)
            for x in ele:
                list_unique_id.append(x.text)
            cage_xpath = '//div[@class="sds-static margin-top-2px"]'
            ele = driver.find_elements(By.XPATH, cage_xpath)
            for x in ele:
                list_cage_code.append(x.text)
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(3)
                next_xpath = '//button[@id="bottomPagination-nextPage"]'
                next_button = driver.find_element(By.XPATH, next_xpath)
                driver.execute_script("arguments[0].click();", next_button)
            except:
                break
        try:
            data = pd.DataFrame()
            data['Unique ID'] = list_unique_id
            data['Name'] = list_name
            data['Status'] = list_status
            data['Address'] = list_physical_address
            data['Classification'] = list_classification
            data['Activation'] = list_activation
            data['Deacivation'] = list_deactivation
            data['Cage Code'] = list_cage_code
            data.to_csv('Samgov_Scraped_data.csv')
            print('CSV File Created successfully')
        except:
            print('Error in Creating CSV File')

    def uk_cabinet_contracts_scraper(self):
        list_name = []
        list_agency = []
        list_desc = []
        list_other_characteristics = []
        url = 'https://www.contractsfinder.service.gov.uk/Search/Results'
        driver.get(url)
        sleep(5)
        while True:
            main_xpath = '//div[@class="search-result"]'
            ele = driver.find_elements(By.XPATH, main_xpath)
            for x in ele:
                print('\n\n', x.text, '\n\n')
                txt = x.text
                txt1 = txt.split('\n')
                list_name.append(txt1[0])
                list_agency.append(txt1[1])
                list_desc.append(txt1[2])
                count = 4
                str1 = str(txt1[3])
                while count < len(txt1):
                    str1 = str1 + ' , ' + str(txt1[count])
                    count += 1
                list_other_characteristics.append(str1)
            try:
                next_xpath = '//a[@class="standard-paginate-next govuk-link break-word"]'
                next_button = driver.find_element(By.XPATH, next_xpath)
                driver.execute_script("arguments[0].click();", next_button)
            except:
                break
        try:
            data = pd.DataFrame()
            data['Name'] = list_name
            data['Agency'] = list_agency
            data['Desc'] = list_desc
            data.to_csv('uk_Scraped_data.csv')
            print('CSV File Created successfully')
        except:
            print('Error in Creating CSV File')

    def california_scraper(self):
        url = 'https://dot.ca.gov/programs/procurement-and-contracts/contracts-out-for-bid'
        driver.get(url)
        ele = driver.find_elements(By.XPATH, '//td')
        list_event_id = []
        list_event_name = []
        list_end_date = []
        count = 0
        while count < len(ele):
            list_event_id.append(ele[count].text)
            count += 3
        count = 1
        while count < len(ele):
            list_event_name.append(ele[count].text)
            count += 3
        count = 2
        while count < len(ele):
            list_end_date.append(ele[count].text)
            count += 3
        try:
            data = pd.DataFrame()
            data['Event Name'] = list_event_name
            data['Event ID'] = list_event_id
            data['End Date'] = list_end_date
            data.to_csv('Claifornia_Scraped_data.csv')
            print('CSV File Created successfully')
        except:
            print('Error in Creating CSV File')

object1 = Scraper()
# Just select one of the following sites to scrape and select the function accordingly
#object1.california_scraper()
object1.samgov_scraper()
#object1.uk_cabinet_contracts_scraper()
#bject1.opentender_scrape()