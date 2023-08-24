# importing the module
from src.scraping.scraper import TenderScraper


if __name__ == '__main__':
    try:
        # url to extract
        url = "https://etenders.gov.in/eprocure/app"

        # Please change the directory before executing the code
        data_dir = '/Volumes/linux/github/scraping_etenders/data'
        
        # Getting the scraper and extracting data
        scraper = TenderScraper(url)
        scraper.get_latest_tenders(export_dir=data_dir)
        scraper.get_data_by_location(location='Delhi', export_dir=data_dir)
    
    except Exception as e:
        print(e)

