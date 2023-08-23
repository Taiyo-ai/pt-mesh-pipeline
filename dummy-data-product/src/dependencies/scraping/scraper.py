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
        closing_link = self.driver.find_element(By.XPATH, '//*[@id="LinkSubmit_1"]')
        closing_link.click()

        #Create data to store the scraped tenders data from website
        data = []

        while True:
            try:
                #Find the table containing the tenders data
                table = self.driver.find_element(By.XPATH, '//*[@id="table"]/tbody')
            
                #Find all the rows in the table
                rows = table.find_elements(By.TAG_NAME, 'tr')

                #Loop through the rows and extract the data from each cell
                for row in rows[1:]:
                    columns = row.find_element(By.TAG_NAME, "td")
                    if len(columns) >= 6:
                        sno = columns[0].text
                        e_published_date = columns[1].text
                        bid_submission_date = columns[2].text
                        tender_opening_date = columns[3].text
                        title_ref = columns[4].text
                        organisation_chain = columns[5].text

                        #append the data to the list
                        data.append([sno, e_published_date, bid_submission_date, tender_opening_date, title_ref, organisation_chain])
                
                #Find the link to the next page
                try:
                    next_page_button = self.driver.find_element(By.ID, "linkFwd")
                except:
                    break

                next_page_button.click()
                WebDriverWait(self.driver, 10).until(EC.staleness_of(table))
                
            except:
                pass

    def driver_close(self):
        self.driver.close()
        self.driver.quit()