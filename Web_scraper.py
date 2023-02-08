import requests
from bs4 import BeautifulSoup
import csv

class TenderScraper:
    def __init__(self, url):
        self.url = url

    def get_tenders(self):
        tenders = []
        # make a GET request to the URL
        response = requests.get(self.url)
        # parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')
        # find all the tender entries on the page
        tender_entries = soup.find_all('tr', {'class': 'table-row'})
        # extract data from each tender entry
        for entry in tender_entries:
            tender = {}
            cells = entry.find_all('td')
            tender['Tender ID'] = cells[0].text
            tender['Tender Title'] = cells[1].text
            tender['Department'] = cells[2].text
            tender['Published On'] = cells[3].text
            tenders.append(tender)
        return tenders

    def write_to_csv(self, tenders, file_name):
        # write the extracted tenders to a CSV file
        with open(file_name, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['Tender ID', 'Tender Title', 'Department', 'Published On'])
            writer.writeheader()
            writer.writerows(tenders)
            
scraper = TenderScraper('https://etenders.gov.in/eprocure/app')
tenders = scraper.get_tenders()
scraper.write_to_csv(tenders, 'C:/Users/admin/Desktop/Web Scraper/tenders.csv')
