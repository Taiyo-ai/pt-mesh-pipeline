from selenium.webdriver.common.by import By
from PIL import Image

import sys
sys.path.insert(0, '/Users/Dell/Documents/My Files/TaiyoAI/pt-mesh-pipeline/dummy-data-product/src/')

from dependencies.scraping.scraper import Scraper
# from scraper import Scraper
from dependencies.cleaning.cleaning import convert_non_black_dots_to_white

import pytesseract
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def scrape_etender_data():
    tender_list = list()

    for val in ['1', '2']:
        scraper = Scraper('https://etenders.gov.in/eprocure/app')
        scraper.click_to_xpath("//span[@id='For']/span[1]/a")
        scraper.select_value_for_xpath("//tr/td/select[@id='TenderType']", val)

        image_path = 'image.png'
        scraper.save_image_from_xpath("//img[@id='captchaImage']", image_path)

        image = plt.imread(image_path)
        image = convert_non_black_dots_to_white(image)
        image = Image.fromarray((image * 255).astype(np.uint8))

        captcha = pytesseract.image_to_string(image, lang='eng')
        captcha = captcha.strip().replace(" ", "")

        scraper.input_text_to_xpath("//input[@id='captchaText']", captcha)
        scraper.click_to_xpath("//input[@id='submit']")

        while True:
            try:
                try:
                    current_tender_id = 'DirectLink_0'
                    current_index = 0
                    while True:
                        title = scraper.find_element(f"//a[@id='{current_tender_id}']")
                        metadata = title.find_element(By.XPATH, f"..").text.strip().split("][")
                        reference_no = metadata[0][1:]
                        tender_id = metadata[1][:-1]

                        tender_list.append((title.text, reference_no, tender_id))
                        current_tender_id = 'DirectLink_0'
                        current_tender_id = current_tender_id + '_' + str(current_index)
                        current_index += 1
                except Exception as e:
                    scraper.click_to_xpath("//a[@id='linkFwd']")

            except:
                break

    tender_df = pd.DataFrame(columns=['title', 'tender_id'], data=tender_list)
    print(tender_df)
    tender_df.to_csv('india_tender_data.csv')