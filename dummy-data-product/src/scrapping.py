from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import requests


class Scrapping:
     # Set up the Chrome webdriver 
    driver = webdriver.Chrome('C:/Users/CF3028TU/Downloads/chromedriver_win32 (1)/chromedriver.exe')
            
    def procurement_csv(self):

       

        # Navigate to the eTenders website
        self.driver.get("https://etenders.gov.in/eprocure/app")

        time.sleep(5)

        # Get the page source after the dynamic content has loaded
        page_source = driver.page_source

        # Parse the content of the page using BeautifulSoup
        soup = BeautifulSoup(page_source, "html.parser")
        rows = soup.find_all('tr', {'class': ['even', 'odd']})

        title=[]
        reference_no = []
        closing_date = []
        bid_opening_date=[]

        for i in range(1, 100):
            link_tag = soup.find('a', {'class': 'link2', 'id': f'DirectLink_{i}'})
            if link_tag is not None:
                link_id = link_tag.get('id')
                link_text = link_tag.text.strip()
                title.append(link_text)

        for row in rows:

            cols = row.find_all('td', {'width': ['20%', '25%', '25%']})

            # extract the text content of the <td> tags and append them to the respective lists
            reference_no.append(cols[0].get_text(strip=True))
            closing_date.append(cols[1].get_text(strip=True))
            bid_opening_date.append(cols[2].get_text(strip=True))

        # Combine the data into a list of tuples
        data = list(zip(title ,reference_no, closing_date, bid_opening_date))

        # Write the data to a CSV file
        with open('procurement.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Title', 'Reference Number', 'Closing Date', 'Bid Opening Date'])
            writer.writerows(data)

        # Close the webdriver
        driver.quit()

        print("CSV suscessfully saved")

        
    def chinabidding(self):
#         driver = webdriver.Chrome('C:/Users/CF3028TU/Downloads/chromedriver_win32 (1)/chromedriver.exe')

        # Navigate to the eTenders website
        self.driver.get("http://en.chinabidding.mofcom.gov.cn/channel/EnSearchList.shtml?tenders=1")

        time.sleep(5)

        # Get the page source after the dynamic content has loaded
        page_source = driver.page_source

        # Parse the content of the page using BeautifulSoup
        soup = BeautifulSoup(page_source, "html.parser")


        data = {}
        items = soup.find_all("div", class_="list-item")
        for item in items:
            title = item.find('a').get_text()
            industry = item.find("div", class_="property").find_all("span")[0].text.strip()
            region = item.find("div", class_="property").find_all("span")[1].text.strip()
            data[title] = {"industry": industry, "region": region}

        # Open a new file to write to
        with open("chinabidding.csv", mode="w", newline="") as csvfile:
            # Define the column names
            fieldnames = ["Title", "Industry", "Region"]
            # Create a CSV writer object
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            # Write the column names as the header row
            writer.writeheader()
            # Write each row of data to the CSV file
            for title, values in data.items():
                industry = values["industry"]
                region = values["region"]
                writer.writerow({"Title": title, "Industry": industry, "Region": region})
            
            
    def chinabiddingen(self):
         # Set up the Chrome webdriver 
#         driver = webdriver.Chrome('C:/Users/CF3028TU/Downloads/chromedriver_win32 (1)/chromedriver.exe')

        # Navigate to the eTenders website
        self.driver.get("https://www.chinabidding.com/en")

        time.sleep(5)

        # Get the page source after the dynamic content has loaded
        page_source = driver.page_source

        # Parse the content of the page using BeautifulSoup
        soup = BeautifulSoup(page_source, "html.parser")




        
        # Find all the list items with the given class
        items = soup.find_all("li", class_="ui-list-item")
        tender_change=soup.find_all("li", class_="ui-list-item fn-clear")


        # Open a CSV file in write mode
        with open("tender_new.csv", "w", newline="") as file:
            writer = csv.writer(file)

            # Write the header row
            writer.writerow(["Title", "URL", "Date"])

            # Loop through each item and extract the title, URL, and date
            for item in items:
                title = item.find("a").text
                url = item.find("a")["href"]
                date = item.find("p", class_="float-right gray").text

                # Write the data into the CSV file
                writer.writerow([title, url, date])

            print("Tender_new Data saved successfully!")


        # Open a CSV file in write mode
        with open("tender_change.csv", "w", newline="") as file:
            writer = csv.writer(file)

            # Write the header row
            writer.writerow(["Title", "URL", "Date"])

            # Loop through each item and extract the title, URL, and date
            for item in tender_change:
                title = item.find("a").text
                url = item.find("a")["href"]
                date = item.find("p", class_="float-right gray").text

                # Write the data into the CSV file
                writer.writerow([title, url, date])

            print(" Tender change Data saved successfully!")
        
        
        
    def searchresult(self):

        url = 'https://www.cpppc.org:8082/inforpublic/homepage.html#/searchresult'
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            print(soup)
        else:
            print(f"Failed to access page. Response code: {response.status_code}")
        



obj = Scrapping()
obj.procurement_csv()
obj.chinabidding()
obj.chinabiddingen()
obj.searchresult()