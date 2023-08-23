from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

class Scraper:
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome()
        self.driver.get(self.url)
        

    def scraping_data(self):
        closing_link = self.driver.find_element(By.ID, "For_1")
        closing_link.click()

        tender_14 = self.driver.find_element(By.XPATH, "//*[@id='LinkSubmit_1']")
        tender_14.click()

        #Create data to store the scraped tenders data from website
        data = []

        while True:
            # try:
            #Find the table containing the tenders data
            table = self.driver.find_element(By.XPATH, '//*[@id="table"]/tbody')
        
            #Find all the rows in the table
            rows = table.find_elements(By.TAG_NAME, 'tr')

            #Loop through the rows and extract the data from each cell
            for row in rows[1:]:  # Skip the header row
                columns = row.find_elements(By.TAG_NAME, "td")
                if len(columns) >= 6:  # Change this to match the number of columns you are actually extracting
                    sno = columns[0].text
                    e_published_date = columns[1].text
                    bid_submission_date = columns[2].text
                    tender_opening_date = columns[3].text
                    title_ref = columns[4].text
                    organisation_chain = columns[5].text  # Uncomment this line if you want to extract this data

                    data.append([sno, e_published_date, bid_submission_date, tender_opening_date, title_ref, organisation_chain])
            
                #Find the link to the next page
            try:
                next_page_button = self.driver.find_element(By.ID, "linkFwd")
            except:
                break

            next_page_button.click()
            WebDriverWait(self.driver, 10).until(EC.staleness_of(table))
                
        self.driver.quit()
        return data 