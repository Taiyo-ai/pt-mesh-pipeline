
# import your dependencies here

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import os
import csv


class Scarper:
    def __init__(self, **kwargs):
        # initialize configuration and chrome driver path to perform data scrapping from website
        self.config = kwargs.get("config")
        self.webdriver_path = self.config.get("webdriver_path")
        self.url = 'https://etenders.gov.in/eprocure/app'
        self.output_file = ''  # Intialize output file

    # Create a directory if it doesn't exist
    def __create_dir(self):
        try:
            os.mkdir('../../data')
        except FileExistsError:
            pass

    # create csv file to store proccess file
    def __create_csv(self):
        try:
            self.output_file = 'eprocurement_india.csv'
        except FileNotFoundError:
            pass

    # scrapping data from website

    def scrap_data(self):
        """Extraction or processing of data"""
        self.__create_dir()
        self.__create_csv()

        # Configure ChromeOptions for headless and incognito browsing
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--incognito")  # Set the browser to run in incognito mode

        # Set up the WebDriver service
        service = Service(self.webdriver_path)

        # Create a WebDriver instance with configured options and service
        driver = webdriver.Chrome(service=service , options=options)

        # Navigate to the specified URL
        driver.get(self.url)

        # Find and click the organization page link
        organization_page = driver.find_element(By.ID , "PageLink_0")
        organization_page.click()

        # Get the page source
        page_source = driver.page_source

        # Parse the page source using BeautifulSoup
        soup = BeautifulSoup(page_source , 'html.parser')

        # Find the table with the specified ID
        table = soup.find('table' , {'id': 'table'})

        # Find all even rows (tr elements) in the table
        even_row = table.find_all('tr')

        # header for the csv file
        header = [
            'Organisation Name' , 'Number of Tenders' ,
            'Organisation Chain' , 'Tender Reference Number' , 'Tender ID' ,
            'Withdrawal Allowed' , 'Tender Type' , 'Form Of Contract' , 'General Technical Evaluation Allowed' ,
            'ItemWise Technical Evaluation Allowed' , 'Payment Mode' , 'Is Multi Currency Allowed For BOQ' ,
            'Is Multi Currency Allowed For Fee' , 'Allow Two Stage Bidding' , 'Tender Category' , 'No. of Covers' ,

            'Tender Fee in Dollars' , 'Fee Payable To' , 'Fee Payable At' , 'Tender Fee Exemption Allowed' ,
            'EMD Amount in Dollars' ,

            'EMD through BG/ST or EMD Exemption Allowed' , 'EMD Fee Type' , 'EMD Percentage' ,
            'EMD Payable To' , 'EMD Payable At' ,

            'Title' , 'Work Description' , 'NDA/Pre Qualification' , 'Independent External Monitor/Remarks' ,
            'Tender Value in Dollars' , 'Product Category' , 'Sub category' , 'Contract Type' , 'Bid Validity(Days)' ,
            'Period Of Work(Days)' , 'Location' , 'Pincode' , 'Pre Bid Meeting Place' , 'Pre Bid Meeting Address' ,
            'Pre Bid Meeting Date' , 'Bid Opening Place' , 'Should Allow NDA Tender' , 'Allow Preferential Bidder' ,

            'Published Date' , 'Bid Opening Date' , 'Document Download / Sale Start Date' ,
            'Document Download / Sale End Date' , 'Clarification Start Date' , 'Clarification End Date' ,
            'Bid Submission Start Date' , 'Bid Submission End Date' ,

            'Name' , 'Address']

        # Open the output file for writing using UTF-16 encoding and tab delimite
        with open('../../data/' + self.output_file , 'w' , newline='' , encoding="utf-16") as file:

            # Create a CSV DictWriter with specified header and delimiter
            writer = csv.DictWriter(file , fieldnames=header , delimiter="\t")

            # Write the header row to the CSV file
            writer.writeheader()

            # Loop through rows in the 'even_row' list, skipping the first one
            for row in even_row[1:]:

                # Find cells within the row using BeautifulSoup
                org_cells = row.find_all('td')

                # Check if cells are found
                if org_cells:

                    # Extract organization name from the second cell
                    org_name = org_cells[1].text.strip()
                    # Extract the number of tenders from the third cell
                    tender_count = int(org_cells[2].text.strip())
                    # Construct the tender link
                    tender_link = "https://etenders.gov.in" + org_cells[2].find('a')['href']
                    # Visit the tender link using a web driver
                    driver.get(tender_link)
                    # Create a nested BeautifulSoup object from the page source
                    nested_soup = BeautifulSoup(driver.page_source , 'html.parser')
                    # Find the additional table with the ID 'table' within the nested soup
                    addition_table = nested_soup.find('table' , {'id': 'table'})
                    # Find all rows within the additional table
                    additional_row = addition_table.find_all('tr')
                    # Loop through rows in the additional table, skipping the first one
                    for j in additional_row[1:]:
                        # Create a dictionary with default values for all header fields
                        default_value = None
                        org_dict = dict.fromkeys(header, default_value)

                        # Populate the organization name and tender count
                        org_dict['Organisation Name'] = org_name
                        org_dict['Number of Tenders'] = tender_count

                        # Iterate through the cells of a table on a web page
                        cells = j.find_all("td")

                        # Check if there are no cells, exit loop if empty
                        if not cells:
                            break
                        else:
                            # Construct detail link using the value in the fourth cell
                            detail_link = "https://etenders.gov.in" + cells[4].find('a')['href']
                            # Open the detail link in the browser driver
                            driver.get(detail_link)
                            # Find all elements with class 'tablebg'
                            content = driver.find_elements(By.CLASS_NAME , 'tablebg')

                            # Iterate through the content found on the detail page
                            for element in content:
                                # Find all 'td' elements within the current element
                                td_elements = element.find_elements(By.TAG_NAME, 'td')

                                # Iterate through the 'td' elements
                                for td_element in td_elements:
                                    text = td_element.text

                                    # Check for specific text patterns to identify sections
                                    if text == 'Organisation Chain':
                                        # Extract data from the table under 'Basic Details' section
                                        tabel1 = element.find_element(By.TAG_NAME, 'tbody')
                                        org_field_name , org_field_values = self.table_data(tabel1)
                                        for key, val in zip(org_field_name , org_field_values):
                                            org_dict[key.text] = val.text
                                        break

                                    elif text == 'Tender Fee in ₹':
                                        # Extract data from the table under 'Tender Fee Details, [Total Fee in ₹ * - 0.00]'	 section
                                        tabel2 = element.find_element(By.TAG_NAME, 'tbody')
                                        org_field_name , org_field_values = self.table_data(tabel2)
                                        for key, val in zip(org_field_name , org_field_values):
                                            org_dict[key.text.replace('₹' , 'Dollars')] = val.text
                                        break
                                    elif text == 'EMD Amount in ₹':
                                        # Extract data from the table under 'EMD Fee Details' section
                                        tabel3 = element.find_element(By.TAG_NAME, 'tbody')
                                        org_field_name , org_field_values = self.table_data(tabel3)
                                        for key, val in zip(org_field_name , org_field_values):
                                            org_dict[key.text.replace('₹' , 'Dollars')] = val.text
                                        break
                                    elif text == 'Title':
                                        # Extract data from the table under 'Title' section
                                        tabel4 = element.find_element(By.TAG_NAME, 'tbody')
                                        org_field_name , org_field_values = self.table_data(tabel4)
                                        for key, val in zip(org_field_name , org_field_values):
                                            org_dict[key.text.replace('₹' , 'Dollars')] = val.text
                                        break
                                    elif text == 'Published Date':
                                        # Extract data from the table under 'Critical Dates' section
                                        tabel5 = element.find_element(By.TAG_NAME, 'tbody')
                                        org_field_name , org_field_values = self.table_data(tabel5)
                                        for key, val in zip(org_field_name , org_field_values):
                                            org_dict[key.text] = val.text
                                        break
                                    elif text == 'Name':
                                        # Extract data from the table under 'Tender Inviting Authority	'
                                        tabel6 = element.find_element(By.TAG_NAME, 'tbody')
                                        org_field_name , org_field_values = self.table_data(tabel6)
                                        for key, val in zip(org_field_name , org_field_values):
                                            org_dict[key.text] = val.text
                                        break
                        # Write the extracted data (org_dict) to a CSV file using the writer
                        writer.writerow(org_dict)
        # Close the browser driver after processing
        driver.quit()

    def table_data(self , table):
        """Function to table data"""
        return table.find_elements(By.CLASS_NAME , 'td_caption') , table.find_elements(By.CLASS_NAME , 'td_field')

    def run(self):
        """Load data, do_something and finally save the data"""
        print("scrapping data started inside scrapper class")
        self.scrap_data()
