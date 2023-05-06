from dependencies.scraping.scraper import Scraper
from dependencies.standardization.standardizer import Standardizer
import os

if __name__ == '__main__':
    url = r'https://www.chinabidding.com/en/info/search.htm'
    scraperObject = Scraper(url)
    scraperObject.request_content()
    file_name = os.path.join(os.getcwd(), 'tenders.csv')
    standardizerObject = Standardizer('tenders.csv').barPlot()