from bs4 import BeautifulSoup
import pandas as pd
import requests
from concurrent.futures import ThreadPoolExecutor



def get_urls(start_url="https://www.contractsfinder.service.gov.uk/Search/Results?page=1#de783605-f321-48f6-bd0b-51e36d5583f3"):
    lis = BeautifulSoup(requests.get(start_url).content,'html.parser').find_all('li',{'class':'standard-paginate'})
    end_num = int(lis[-1].text)
    urls = []
    for i in range(1,end_num + 1):
        urls.append(f"https://www.contractsfinder.service.gov.uk/Search/Results?page={i}#de783605-f321-48f6-bd0b-51e36d5583f3")
    return urls




class ScrapeContracts:

    def __init__(self,url):
        self.url = url
        self.soup = BeautifulSoup(requests.get(self.url).content,'html.parser')
        self.search_results = self.soup.find_all('div',{'class':'search-result'})

    
    def __info_per_div(self,search_res):
        info_dict = dict()
        url_title = search_res.find('div',{'class':'search-result-header'})
        info_dict['Title'] = url_title.text
        info_dict['URL'] = url_title.find('a')['href']
        info_dict['Description'] = search_res.find('div',{'class':'wrap-text'}).text
        search_entries = search_res.find_all('div',{'class':'search-result-entry'})

        for se in search_entries:
            #print(se)
            info_dict[se.find('strong').text] = se.contents[-1].strip()

        return info_dict

    def get_info(self):
        info = []
        for sr in self.search_results:
            
            info.append(self.__info_per_div(sr))
        
        return info



if __name__ == "__main__":
    res = []
    urls = get_urls()
    def append_scraped_res(url):
        sc = ScrapeContracts(url)
        res.append(sc.get_info())

    with ThreadPoolExecutor() as f:
        f.map(append_scraped_res,urls)

    res = sum(res,[])
    df = pd.DataFrame(res)
    print(df.head())
    df.to_csv('collected_contracts.csv')
