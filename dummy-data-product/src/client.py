import logging

from datetime import datetime

# Importing scraping and data processing modules
from dependencies.scraping.scraper import Scraper
from dependencies.cleaning.cleaning import CleanData
from dependencies.standardization.standardizer import Standardize_data

logging.basicConfig(level=logging.INFO)


class FetchCSVfile:
    def __init__(self, **kwargs):
        self.config = kwargs.get('config')

    def step1(self):
        '''Load and Extract Data'''
        extraction_obj = Scraper(config=self.config)
        raw_extracted_data_path = extraction_obj.download_tenders()
        return raw_extracted_data_path

    def step2(self):
        '''Clean the Extracted Data'''
        regulating_obj = CleanData(config=self.regulating_config)
        cleansed_files_path = regulating_obj.sanitize_csv_files()
        return cleansed_files_path

    def step3(self):
        '''Merge all the cleansed files'''
        st_obj = Standardize_data(cleaned_data=self.standardize_config)
        st_obj.generate_standardize_data()

    def run(self):
        self.regulating_config = self.step1()
        self.regulating_config['country_code_conversion_cell_idx'] = self.config['country_code_conversion_cell_idx']

        self.standardize_config = self.step2()
        self.step3()


if __name__ == "__main__":
    config = {
        'site_url': 'https://opentender.eu',
        'scraping_url': 'https://opentender.eu/download',
        'scarping_keywords': {
            'parent_row': ('div', 'download-row'),
            'country_name': ('h1', 'download-name'),
            'download_link_class': 'download-column download-csv'
        },
        'path_config': {
            'country_csv_url_map': r'dummy-data-product/src/dependencies/utils/country_csv_url_map.json'
        },
        'country_code_conversion_cell_idx': [2, 99, 136]
    }
    # Refer to "dependencies\utils\country_csv_url_map.json" for country names.
    country_list = ['Malta', 'Cyprus']
    config['country_list'] = country_list

    main_obj = FetchCSVfile(config=config)
    main_obj.run()

    logging.info(
        {
            "last_executed": str(datetime.now()),
            "status": "Pipeline executed successfully",
        }
    )
