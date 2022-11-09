import csv
import pycountry
import os
import logging


logging.basicConfig(level=logging.INFO)

class CleanData:
    def __init__(self, **kwargs):
        self.config = kwargs.get('config')

    def convert_country_code(self, csv_row):
        for idx in self.config['country_code_conversion_cell_idx']:
            country = pycountry.countries.get(alpha_2=csv_row[idx])
            if country and country.alpha_2 == csv_row[idx]:
                csv_row[idx] = country.alpha_3
        return csv_row

    def replace_missing_values(self, csv_row):
        for idx, val in enumerate(csv_row):
            if val == '':
                csv_row[idx] = '##empty'    # Uniform value for all empty cells.
        return csv_row

    def sanitize_csv_files(self):
        for country in self.config['raw_data_path']:
            raw_data_dir_path = self.config['raw_data_path'][country]
            output_dir_path = 'data/%s/cleaned_data' % country
            if not os.path.exists(output_dir_path):
                os.makedirs(output_dir_path)

            for filename in os.listdir(raw_data_dir_path):
                with open('%s/%s' % (raw_data_dir_path, filename), 'r', encoding='utf-8') as file:
                    loadedCsv = list(csv.reader(file, delimiter=';'))
                    for idx, row in enumerate(loadedCsv):
                        loadedCsv[idx] = self.replace_missing_values(self.convert_country_code(row))[1:]

                    file_path = '%s/%s' % (output_dir_path, filename)
                    with open(file_path, 'w', encoding='utf-8', newline='') as outfile:
                        csvwriter = csv.writer(outfile)
                        csvwriter.writerows(loadedCsv)
            if 'cleaned_data' not in self.config:
                self.config['cleaned_data'] = dict()
            self.config['cleaned_data'][country] = output_dir_path
            logging.info(f'Sanitized CSV files for {country}')
        return self.config['cleaned_data']


if __name__ == '__main__':
    config = {
        'raw_data_path': {'Malta': 'data/Malta/raw_data', 'Cyprus': 'data/Cyprus/raw_data'},
        'country_code_conversion_cell_idx': [2, 99, 136]
    }
    ob = CleanData(config=config)
