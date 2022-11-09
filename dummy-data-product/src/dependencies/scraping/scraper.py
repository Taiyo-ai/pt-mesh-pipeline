from bs4 import BeautifulSoup
import requests
import json
import os
import shutil

class Scraper:
    def __init__(self, contry_list, **kwargs):
        self.contry_list = contry_list
        self.config = kwargs.get('config')

    def generate_country_csv_url_map(self):
        scraping_url = self.config.get('scraping_url')

        country_csv_url_map = dict()

        resp = requests.get(scraping_url)
        soup = BeautifulSoup(resp.content, 'html5lib')

        all_rows = soup.find_all(self.config['scarping_keywords']['parent_row'][0], class_=self.config['scarping_keywords']['parent_row'][1])
        for row in all_rows:
            country_name = row.find(self.config['scarping_keywords']['country_name'][0], class_=self.config['scarping_keywords']['country_name'][1]).text
            csv_download_link = row.find(class_=self.config['scarping_keywords']['download_link_class']).find('a', href=True).get('href')
            if country_name and csv_download_link:
                country_csv_url_map[country_name.strip()] = csv_download_link.strip()

        with open(self.config['path_config']['country_csv_url_map'], 'w', encoding='utf-8') as f:
            json.dump(country_csv_url_map, f)
        return country_csv_url_map

    def download_tenders(self):
        country_csv_url_map = self.generate_country_csv_url_map()
        for country in self.contry_list:
            if country not in country_csv_url_map:
                continue
            csv_download_url = country_csv_url_map[country]
            storage_path = 'data\%s\\raw_data' % country
            zip_file_path = '%s/%s.zip' % (storage_path, country)

            resp = requests.get('%s%s' % (self.config['site_url'], csv_download_url))

            if not os.path.exists(storage_path):
                os.makedirs(storage_path)
            with open(zip_file_path, 'wb') as fh:
                fh.write(resp.content)

            shutil.unpack_archive(zip_file_path, storage_path)
            os.remove(zip_file_path)

            if 'raw_data_path' not in self.config['path_config']:
                self.config['path_config']['raw_data_path'] = dict()
            self.config['path_config']['raw_data_path'][country] = storage_path
        return self.config['path_config']


if __name__ == '__main__':
    config = {
        'site_url': 'https://opentender.eu',
        'scraping_url': 'https://opentender.eu/download',
        'scarping_keywords': {
            'parent_row': ('div', 'download-row'),
            'country_name': ('h1', 'download-name'),
            'download_link_class': 'download-column download-csv'
        },
        'path_config': {
            'country_csv_url_map': r'dummy-data-product\src\dependencies\utils\country_csv_url_map.json'
        }

    }
    country_list = ['Malta', 'Cyprus']
    ob = Scraper(country_list, config=config)
    raw_data_path = ob.download_tenders()