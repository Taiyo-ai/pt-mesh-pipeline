
from dependencies.scraping import Scraper

scraping = Scraper()
data = scraping.extract()

print(data)