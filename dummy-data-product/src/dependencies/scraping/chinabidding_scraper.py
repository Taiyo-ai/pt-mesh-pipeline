from selenium.webdriver.common.by import By

import pandas as pd

import sys
sys.path.insert(0, '/Users/Dell/Documents/My Files/TaiyoAI/pt-mesh-pipeline/dummy-data-product/src/')

from dependencies.scraping.scraper import Scraper
# from scraper import Scraper

def scrape_chinabidding_data():
    scraper = Scraper('https://www.chinabidding.com/en/info/search.htm')

    tender_list = list()
    is_first = True

    while True:
        try:
            # tender_element = driver.find_elements(By.XPATH, "//li[@class='list-item']")
            tender_element = scraper.find_elements("//li[@class='list-item']")
            for tender in tender_element:
                title = tender.find_element(By.XPATH, ".//a[@class='item-title-text bold fs18']")
                industry_region = tender.find_elements(By.XPATH, ".//div[@class='item-link']/span")
                
                assert len(industry_region) == 2
                industry = industry_region[0].text.split("：")[1].strip()
                region = industry_region[1].text.split("：")[1].strip()
                # print(title.text, 'Industry:', industry, 'Region:', region)
                tender_list.append((title.text, industry, region))
            
            # bar = driver.find_elements(By.XPATH, "//a[@class='page-link next']")
            bar = scraper.find_elements("//a[@class='page-link next']")
            if len(bar) == 2:
                bar[-1].click()
            elif is_first:
                is_first = False
                bar[-1].click()
            else:
                break

        except Exception as e:
            print(e)
            break

    tender_df = pd.DataFrame(columns=['title', 'industry', 'region'], data=tender_list)
    print(tender_df)
    tender_df.to_csv('chinabidding_tenders.csv')