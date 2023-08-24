import datetime
import time
import os
import warnings

import pandas as pd
import requests
import urllib

from bs4 import BeautifulSoup
from captcha_solver import CaptchaSolver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

warnings.filterwarnings('ignore')

__all__ = ['TenderScraper']

class TenderScraper:
    def __init__(self, url):
        self.url = url

    def get_latest_tenders(self, export_dir=None):
        try:
            if export_dir is not None and os.path.exists(export_dir):
                # Initializing the soup
                resp = requests.get(self.url)
                soup = BeautifulSoup(resp.text, 'lxml')

                # Finding the table
                table = soup.find_all(id='marqueecontainer')
                columns = ['Tender Title', 'Reference No', 'Closing Date', 'Bid Opening Date']
                df = pd.read_html(str(table))[0]
                df.columns = columns

                # Path for saving data
                data_path = os.path.abspath(export_dir)
                file_path = f'latest_tenders_{datetime.date.today().strftime("%d_%m_%Y")}.csv'
                #save_path = f'{data_path}/latest_tenders_{datetime.date.today().strftime("%d_%m_%Y")}.csv'
                save_path = os.path.join(data_path, file_path)

                # Exporting data to CSV file
                df.to_csv(save_path, index=False)
                print(f"Latest tenders data extracted to: {save_path}")
            else:
                print("Path not exist")


        except Exception as e:
            print(e)

    def get_data_by_location(self, location=None, export_dir=None):
        try:
            if export_dir is not None and os.path.exists(export_dir):
                # Getting the web driver
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_argument('disable-notifications')

                driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
                driver.get(self.url)

                # Navigating to the page
                location_link = driver.find_element(By.ID, 'PageLink').click()
                driver.find_element(By.XPATH, '//*[@id="Location"]').send_keys(location.lower())
                time.sleep(5)

                # reading the captcha image and downloading
                img = driver.find_element(By.XPATH,'//*[@id="captchaImage"]')
                src = img.get_attribute('src')
                urllib.request.urlretrieve(src, "captcha.png")

                # Giving input for captcha
                solver = CaptchaSolver('browser')
                raw_data = open('captcha.png', 'rb').read()
                captcha_input = solver.solve_captcha(raw_data)

                # Sending input to captcha input and submit
                driver.find_element(By.XPATH, '//*[@id="captchaText"]').send_keys(captcha_input)
                time.sleep(5)
                driver.find_element(By.XPATH, '//*[@id="submit"]').click()

                # Removing captcha file
                os.remove('captcha.png')

                # Getting the table data
                table_data = driver.find_element(By.XPATH, '//*[@id="table"]')
                soup = BeautifulSoup(table_data.get_attribute("outerHTML"), 'lxml')
                df = pd.read_html(str(soup), header=0)[0]
                df = df.dropna(axis=1, how="all")

                # Path for saving data
                data_path = os.path.abspath(export_dir)
                file_path = f'{location.lower()}_tenders_{datetime.date.today().strftime("%d_%m_%Y")}.csv'
                #save_path = f'{data_path}/{location.lower()}_tenders_{datetime.date.today().strftime("%d_%m_%Y")}.csv'
                save_path = os.path.join(data_path, file_path)

                # Exporting data to CSV file
                df.to_csv(save_path, index=False)
                print(f"{location.capitalize()} location tenders data extracted to: {save_path}")

            else:
                print("Path not exist")

        except Exception as e:
            print(e)

        finally:
            driver.quit()


if __name__ == '__main__':

    url = "https://etenders.gov.in/eprocure/app"

    scraper = TenderScraper(url)
    scraper.get_latest_tenders()
    scraper.get_data_by_location('Delhi')
