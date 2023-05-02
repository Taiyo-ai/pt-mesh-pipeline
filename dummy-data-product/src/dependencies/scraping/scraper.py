import urllib.request
from html_table_parser.parser import HTMLTableParser
import pandas as pd

class EprocureScraper:
    
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
        df.drop([0,1], inplace=True)
        df = df.reset_index(drop=True)
        headers = df.iloc[0]
        df  = pd.DataFrame(df.values[1:], columns=headers)
        regex_pat = re.compile(r'([0-9]+[,.])', flags=re.IGNORECASE)
        df['Tender Title'] = df['Tender Title'].str.replace(regex_pat, '', regex=True)
        df['Closing Date'] = pd.to_datetime(df['Closing Date'])
        df['Bid Opening Date'] = pd.to_datetime(df['Bid Opening Date'])
        return df
    
    def save_to_csv(self, file_name):
        df = self.scrape_data()
        df.to_csv(file_name, index=False)
