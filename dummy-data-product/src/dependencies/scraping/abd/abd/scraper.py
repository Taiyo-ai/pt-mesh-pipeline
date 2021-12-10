from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from datetime import datetime as dt

if __name__ == "__main__":
  t = dt.now().strftime(r'%d-%m-%Y %H-%M-%S')
  name = 'results '+t+'.json'

  s = get_project_settings()
  s['FEED_FORMAT'] = 'json'
  s['FEED_URI'] = name
  process = CrawlerProcess(s)
  # 'followall' is the name of one of the spiders of the project.
  process.crawl('abd_spider')
  process.start()
