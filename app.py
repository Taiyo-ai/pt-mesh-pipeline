# Aman Rohilla
# a.rohillaaman@gmail.com
# 8221832254
# Taiyo Intershala Assignment

from bs4 import BeautifulSoup
import requests
import csv

class Scraper:

  def __init__(self, url, filename):
    self.url = url
    self.filename = filename

  def scrape(self):
    if self.url.find('://') != -1:
      res = requests.get(self.url)
      html = res.text
    else:
      with open(self.url) as file:
        html = file.read()

    soup = BeautifulSoup(html, 'html.parser')
    events = []

    for child in soup.find('table').find('tbody').findChildren('tr'):
      tds = child.findChildren('td')
      a_tag = tds[0].findChild('a')
      url = a_tag['href']
      event_id = a_tag.get_text()

      event_name = tds[1].get_text()
      end_date = tds[2].get_text().replace('\n', '')

      events.append([event_id, event_name, end_date, url])

    if(len(events) == 0):
      return

    with open(self.filename, 'w', newline='') as f:
      writer = csv.writer(f)
      writer.writerow(['event_id', 'event_name', 'end_date', 'url'])
      writer.writerows(events)

if __name__ == "__main__":
  scraper = Scraper('https://dot.ca.gov/programs/procurement-and-contracts/contracts-out-for-bid', 'events.csv')
  scraper.scrape()
  print('Scraping Successful, scraped data has been written to events.csv')