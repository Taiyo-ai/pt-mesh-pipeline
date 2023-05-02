import urllib.request
from html_table_parser.parser import HTMLTableParser
import pandas as pd

class Scraper:
    
    def __init__(self, url):
        self.url = url
    
    def url_get_contents(self):
        req = urllib.request.Request(url=self.url)
        f = urllib.request.urlopen(req)
        return f.read().decode('utf-8')

    def scrape_data(self):
        xhtml = self.url_get_contents()
        p = HTMLTableParser()
        p.feed(xhtml)
        df = pd.DataFrame(p.tables[10])
        return df
    
    def save_to_csv(self, file_name):
        df = self.scrape_data()
        df.to_csv(file_name, index=False)
