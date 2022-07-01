'''This script uses pickapp/tor-proxy docker image to creeate tor proxies. If you do not want to use tor proxies remove the arguments of run method in main :
        scraper.run(True) -> scraper.run()

The script crawls the uk cabinet contracts from 'https://www.contractsfinder.service.gov.uk' and stores the data in a 'Result.csv' file 
'''

import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from python_on_whales import DockerClient


class Scraper:
    def __init__(self):
        self.total_pages = None
        self.proxy_list = None
        self.docker = None
        self.url = 'https://www.contractsfinder.service.gov.uk/Search/Results?&page='
        self.records = []
    
    # Method to create docker config file
    #
    def create_proxies(self):
        container_names = ['taiyo-1', 'taiyo-2', 'taiyo-3', 'taiyo-4', 'taiyo-5', 'taiyo-6', 'taiyo-7', 'taiyo-8', 'taiyo-9', 'taiyo-10']
        proxy_list = []

        os.mkdir('Docker_config')
        with open("Docker_config\docker-compose.yml", "w") as f:
            f.write("version: '3'\n\nservices:\n")

            for index, name in enumerate(container_names):
                f.write(f"  tor-{name}:\n")
                f.write(f"    container_name: 'tor-{name}'\n")
                f.write("    image: 'pickapp/tor-proxy:latest'\n")
                f.write("    ports:\n")
                f.write(f"      - '{9990 + index}:8888'\n")
                f.write("    environment:\n")
                f.write("      - IP_CHANGE_SECONDS=60\n")
                f.write("    restart: always\n")
                proxy_list.append(f'http://127.0.0.1:{9990 + index}')

        return proxy_list

    def run_container(self):
        self.proxy_list = self.create_proxies()
        self.docker = DockerClient(compose_files=['./Docker_config/docker-compose.yml'])
        self.docker.compose.up(detach=True)
    
    # Getting webpages
    #
    def scrape_page_1(self):
        page = requests.post(url=self.url + '1')
        soup = BeautifulSoup(page.content, 'html.parser')
        self.total_pages = int(soup.find_all('li', {'class': 'standard-paginate'})[-1].text.strip())
        for contract in soup.find_all('div', {'class': 'search-result'}):
            self.process(contract)
        print(f"Scraped page : 1")

    def scrape_with_docker(self):
        for i in range(2, self.total_pages+1):
            proxies = {'http': self.proxy_list[i % 10]}
            page = requests.post(url=self.url + f'{i}', proxies=proxies)
            soup = BeautifulSoup(page.content, 'html.parser')
            for contract in soup.find_all('div', {'class': 'search-result'}):
                self.process(contract)

            print(f"Scraped page : {i}")
    
    # Method to get webpages without using tor proxies
    #
    def scrape_without_docker(self):
        for i in range(2, self.total_pages + 1):
            page = requests.post(url=self.url+f'{i}')
            soup = BeautifulSoup(page.content, 'html.parser')
            for contract in soup.find_all('div', {'class': 'search-result'}):
                self.process(contract)

            print(f"Scraped page : {i}")

    # Processing the pages to get required data
    #
    def process(self, contract):
        record = {'Title': contract.find('div', {'class': 'search-result-header'}).get('title'),
                  'contract_link': contract.find('a').get('href'),
                  'organisation': contract.find('div', {'class': 'search-result-sub-header wrap-text'}).text}
        try:
            span = contract.find_all('div', {'class': 'wrap-text'})[1].find('span').get('title')
        except AttributeError:
            span = ''
        txt = '' + contract.find_all('div', {'class': 'wrap-text'})[1].text
        record['Description'] = span if txt[:-3] in span else txt

        for result in contract.find_all('div', {'class': 'search-result-entry'}):
            header = result.find('strong').text.strip()
            value = result.text.replace(header, '').strip()
            record[header] = value
        self.records.append(record)

    # Main driver meethod
    #
    def run(self, use_docker=False):
        self.scrape_page_1()
        if use_docker:
            self.run_container()
            self.scrape_with_docker()
            self.docker.compose.down()
        else:
            self.scrape_without_docker()

        print('Scraping Finished\n')
        
         #Saving the data
        pd.DataFrame(self.records).to_csv('Result.csv')


if __name__ == '__main__':
    spider = Scraper()
    spider.run(True)        # currently using tor proxies
