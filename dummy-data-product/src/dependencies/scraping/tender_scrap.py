import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd







class Scrapper:
    
    def total_page_counter(self,arg):
        """Gets number of pages . arg = driver """
        driver = arg
        total_page_xpath = "//*[@id=\"app\"]/search/search_tender/div[3]/div/tender-table/pagination/div[1]/div"
        total_page = driver.find_element(By.XPATH, total_page_xpath)
        r = total_page.text[10:20]
        total_page_count = int(''.join(x for x in r if x.isdigit()))
        return total_page_count



    def get_data_page(self,driver,rows,column,counter):
        """Gets data from one page, writes to csv  and clicks the next page button"""

        table_data = []
        for r in range(1,rows+1):
            row_data = []

            for c in range(1,column+1):
                if c == 1:  #Getting URL! similarly we can add more conditions here, to get data specific to columns.
                    value =  driver.find_element(By.XPATH,"//*[@id=\"table-top\"]/tbody/tr["+str(r)+"]/td["+str(c)+"]/div/div/a" ).get_attribute("href")  
                else:
                    value = driver.find_element(By.XPATH,"//*[@id=\"table-top\"]/tbody/tr["+str(r)+"]/td["+str(c)+"]" ).text.strip()
                row_data.append(value)

            table_data.append(row_data)

            #write the table_data to csv
            df = pd.DataFrame(table_data)
            df.to_csv(f'file{counter}.csv',index = False)

        next_page_button = driver.find_element(By.CLASS_NAME, "page-next")
        webdriver.ActionChains(driver).move_to_element(next_page_button).click(next_page_button).perform()
        time.sleep(2)

            
            
            



    def scrap_all(self,d,r,c):
        """arg1 -> driver , arg2 -> rows, arg3 -> column"""
#         c=column
#         r=rows
#         d=driver
        total_page_count = self.total_page_counter(d)
        counter = 1
        while counter <=total_page_count:
            self.get_data_page(d,r,c,counter)
            counter+=1
            
            
            
    def start(self):
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install())) # 6mb Download. 
        driver.get("https://opentender.eu/all/search/tender")

        time.sleep(2) #waiting for page to load 

        #for hidden elements
        #driver.set_window_size(1024, 600)
        #driver.maximize_window()


        # Can use this to select more column fields, for now i am only extracting the basic data without selecting any columns.
        """
        column_button_xpath = "XPATH of column field to add"
        column_button_element = driver.find_element(By.XPATH, column_button_xpath)
        webdriver.ActionChains(driver).move_to_element(column_button_element).click(column_button_element).perform()
        
        """

        #selecting 100 rows. per page
        more_result_xpath = "//*[@id=\"entriesonpage\"]"
        result_element = driver.find_element(By.XPATH, more_result_xpath)
        webdriver.ActionChains(driver).move_to_element(result_element ).click(result_element).perform()

        result_element.send_keys(Keys.ARROW_DOWN)
        result_element.send_keys(Keys.ARROW_DOWN)
        result_element.send_keys(Keys.ARROW_DOWN)
        result_element.send_keys(Keys.ENTER)


        time.sleep(2) #waiting for all the 100 rows to load
        
        table_rows_xpath = "//*[@id=\"table-top\"]/tbody/tr"
        table_rows_element = driver.find_elements(By.XPATH, table_rows_xpath)

        rows = len(table_rows_element) #count number of rows

        td_xpath = "//*[@id=\"table-top\"]/tbody/tr[1]/td"
        column = len(driver.find_elements(By.XPATH, td_xpath)) #count number of columns in each row
        
        
        
        self.scrap_all(driver,rows,column)
        
        
        
a = Scrapper()
a.start()