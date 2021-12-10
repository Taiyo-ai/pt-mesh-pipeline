from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

if __name__ == "__main__":
  process = CrawlerProcess(get_project_settings())
  # 'followall' is the name of one of the spiders of the project.
  process.crawl('abd_spider')
  process.start()
