import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


class TenderScraper:
    def __init__(self, geckodriver_path, url):
        self.geckodriver_path = geckodriver_path
        self.url = url
        self.options = Options()
        self.options.headless = True
        self.driver = None

    def start(self):
        self.driver = webdriver.Firefox(
            executable_path=self.geckodriver_path, options=self.options)
        self.driver.get(self.url)
        self.driver.maximize_window()

    def extract_tender_info(self, row_data):
        sno = re.findall(r'\b\d+\.\s', row_data)
        row_data = re.sub(r'\b\d+\.\s', '', row_data)
        all_dates = re.findall(r'\d{1,2}-[A-Za-z]{3}-\d{4} \d{2}:\d{2} [APap][Mm]', row_data)
        row_data = re.sub(r'\d{1,2}-[A-Za-z]{3}-\d{4} \d{2}:\d{2} [APap][Mm]', '', row_data)
        two_brkt = re.findall(r'\[.*?\] \[.*?\]', row_data)
        row_data = re.sub(r'\[.*?\] \[.*?\]', '', row_data)
        last_brkt = re.findall(r'\[.*?\]', row_data)
        row_data = re.sub(r'\[.*?\]', '', row_data)

        return [sno[0].strip(), all_dates[0], all_dates[1], all_dates[2], 
                f"{two_brkt[0]} {last_brkt[0]}", row_data.strip()]

    def scrape_tenders(self):
        try:
            data = []
            while True:
                wait = WebDriverWait(self.driver, 10)
                span_element = wait.until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="LinkSubmit_1"]/span')))
                span_element.click()

                rows = wait.until(EC.presence_of_all_elements_located(
                    (By.CSS_SELECTOR, 'tr.odd, tr.even')))

                for row in rows:
                    row_data = row.text
                    
                    tender_info = self.extract_tender_info(row_data)
                    
                    if tender_info:
                        data.append(tender_info)

                link_element = self.driver.find_elements(By.ID, "linkFwd")
                if not link_element:
                    break

                link_element[0].click()

            return data

        except NoSuchElementException:
            print("No more new data to load.")
        finally:
            self.driver.quit()
