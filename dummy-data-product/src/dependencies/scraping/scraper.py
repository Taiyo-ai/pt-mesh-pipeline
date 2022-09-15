from bs4 import BeautifulSoup as bs
import requests
import lxml
import pandas as pd

data = {
        'Tender': [],
        'Company': [],
        'Procurement': [],
        'Notice': [],
        'Location': [],
        'Closing': [],
        'Value': [],
        'Date': [],
        'Tender_Url': []
        }

class Scrapper:
  '''
  Extract data from UK Gov Tenders website and export into .csv file format.
  '''
  def export_to_csv(self, data):
    table = pd.DataFrame(data)
    table.to_csv('UK_Tender_Data.csv', sep=',', encoding='utf-8', index=False)

  def get_tenders_attributes(self, tenders):
    # Getting the  attributes
    data["Tender_Url"].append(tenders.find("a", {"class": ["govuk-link", "search-result-rwh", "break-word"]}).get('href'))
    data["Tender"].append(tenders.find("a", {"class": ["govuk-link", "search-result-rwh", "break-word"]}).text)
    data["Company"].append(tenders.find("div", {"class": ["search-result-sub-header", "wrap-test"]}).text)
    data["Procurement"].append(tenders.find_all("div", {"class": "search-result-entry"})[0].text.replace("Procurement stage", " "))
    data["Notice"].append(tenders.find_all("div", {"class": "search-result-entry"})[1].text.replace("Notice status", " "))
    data["Location"].append(tenders.find_all("div", {"class": "search-result-entry"})[3].text.replace("Contract location", " "))
    try:
      data["Closing"].append(tenders.find_all("div", {"class": "search-result-entry"})[2].text.replace("Closing", " "))
    except:
      data["Closing"].append("None")
    try:
      data["Value"].append(tenders.find_all("div", {"class": "search-result-entry"})[4].text.replace("Total value", " "))
    except:
      data["Value"].append("None")
    try:
      data["Date"].append(tenders.find_all("div", {"class": "search-result-entry"})[5].text.replace("Publication date", " "))
    except:
      data["Date"].append("None")
    
    return data

  def parse_page(self, next_url):
    # HTTP GET requests
    page = requests.get(next_url)
    # Checking if we successfully fetched the URL
    if page.status_code == 200:
      soup = bs(page.text, 'lxml')
      # Fetching all items
      list_all_tenders = soup.find_all("div", {"class" : "search-result"})
      for tenders in list_all_tenders:
        self.get_tenders_attributes(tenders)
    next_page_text = soup.find('ul', class_="gadget-footer-paginate").findAll('li')[-1].text
    if 'Next' in next_page_text:
        next_page_partial = soup.find('ul', class_="gadget-footer-paginate").findAll('li')[-1].find('a')['href']
        self.parse_page(next_page_partial)
    else:
        print("Fetching done.")

  def scraper(self, url):
    print("Fetching pages. Wait, please...")
    self.parse_page(url)
    print("Exporting to csv...")
    self.export_to_csv(data)
    print("Export finished, scraping done.")

obj = Scrapper()
obj.scraper("https://www.contractsfinder.service.gov.uk/Search/Results")
