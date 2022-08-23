# Web Scraping on Public Contracts Scotland Website

# importing Required libraries

import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import pandas as pd

# Assigning web driver

chrome = 'C:\Developer\chromedriver.exe'

driver = webdriver.Chrome(executable_path=chrome)

url = 'https://www.publiccontractsscotland.gov.uk/search/search_mainpage.aspx'

# creating a pandas Dataframe
df3 = pd.DataFrame()

driver.get(url)

# Finding Total pages
total_pages = driver.find_element(by='xpath', value='//*[@id="ctl00_maincontent_PagingHelperBottom_pnlSummary"]'
                                                    '/strong[2]').text
i = 0

while True:
    if i < total_pages:

        # Select required table Element
        table = driver.find_element(by='id', value='maintablecontent')
        rd = []

        # Scraping the data from table and save to a list
        for row in table.find_elements(by='tag name', value='tr'):
            col = row.find_elements(by='tag name', value='td')
            col = [element.text.split('\n') for element in col]
            rd.append(col)

        # First item is empty so it is removed and create a dataframe using the list
        rd = rd[1:]
        df = pd.DataFrame(rd)
        df1 = pd.DataFrame(list(df[1]))
        df2 = pd.concat([df, df1], axis=1)
        df2 = df2.drop([1], axis=1)
        df2.columns.values[1] = 1
        df2[0] = df[0].str.get(0)

        # finding the links to each tender and scrape and save it in a list
        all_links = table.find_elements(by='tag name', value='a')
        final_links = []
        for link in all_links:
            href = link.get_attribute('href')
            if 'https' not in href:
                final_links.append(f'https://www.publiccontractsscotland.gov.uk{href}')
            else:
                final_links.append(href)

        # adding the url list to above dataset as new column and save the dataset as a .csv file
        df2['url'] = final_links
        df3 = df3.append(df2, ignore_index=True)
        df3.to_csv('scrape.csv')

        # Pagination - move to next page
        drop_down = driver.find_element(by="id", value="ctl00_maincontent_PagingHelperBottom_ddPageSelect")
        select = Select(drop_down)
        i += 1
        select.select_by_index(i)
        time.sleep(5)

    else:
        driver.quit()
        print(f'Scraping Completed of {total_pages}')
        break

df3.to_csv('final_scrape.csv')

# Thank You !
