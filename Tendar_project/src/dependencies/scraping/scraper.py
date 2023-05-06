# from functions_ import *
import os
import sys
from Tendar_project.src.dependencies.cleaning.cleaner import Cleaner
import requests
from bs4 import BeautifulSoup

class Scraper():
    def __init__(self, url):
        self.url = url

    @staticmethod
    def save_html(soup, file_name):
        file_path = os.path.join(os.getcwd(), 'Html')
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        with open(fr'Html\\{file_name}.html', 'w', encoding='utf-8') as file:
            file.write(str(soup))

    @staticmethod
    def open_html(file_name, folder_name):
        with open(fr'{folder_name}\\{file_name}.html', 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file.read(), 'html.parser')
        return soup

    def request_content(self):
        session = requests.session()
        nav_num = 1
        while True:
            header = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.64"
            }
            payload = {
                    'fullText': '',
                    'infoClassCodes': 'e0905',
                    'tradeClassCodes': '',
                    'zone': '',
                    'fundSourceCodes': '',
                    'poClass': '',
                    'currentPage': fr'{nav_num}'
                     }
            file_name = fr'page_{nav_num}'
            try:
                soup = self.open_html(file_name, 'Html')
            except:
                req = session.post(url=self.url, headers=header,data=payload)
                soup = BeautifulSoup(req.text, 'html.parser')
                self.save_html(soup, file_name)

            tenders_details = soup.find_all('li', class_='list-item')
            for tenders_detail in tenders_details:
                tender_url = tenders_detail.find('a', class_='item-title-text bold fs18')['href']
                tender_file_name = fr"Tender_{tender_url.split('-')[0].split('/')[-1]}"
                print(tender_file_name)
                try:
                    tender_soup = self.open_html(tender_file_name, 'Html')
                except:
                    req_tender = session.get(tender_url, headers=header)
                    tender_soup = BeautifulSoup(req_tender.text, 'html.parser')
                    self.save_html(tender_soup, tender_file_name)
                cleaner_object = Cleaner(tender_soup, tender_url)
                cleaner_object.dump_data_to_csv()

            if soup.find('div', class_='item-title clearfix') is None:
                break
            print(nav_num)
            # cleaner(soup)
            nav_num += 1


