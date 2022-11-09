import csv
import os
import logging


logging.basicConfig(level=logging.INFO)

class Standardize_data:
    def __init__(self, **kwargs):
        self.cleaned_data = kwargs.get('cleaned_data')

    def generate_standardize_data(self):
        for country in self.cleaned_data:
            cleaned_data_dir_path = self.cleaned_data[country]
            output_dir_path = 'data/%s/standardized_data' % country
            output_file_path = '%s/standardized_data.csv' % (output_dir_path)
            if not os.path.exists(output_dir_path):
                os.makedirs(output_dir_path)
            if os.path.exists(output_file_path):
                os.remove(output_file_path)
            for fidx, filename in enumerate(os.listdir(cleaned_data_dir_path)):
                with open('%s/%s' % (cleaned_data_dir_path, filename), 'r', encoding='utf-8') as file:
                    loadedCsv = csv.reader(file)
                    if fidx != 0:
                        next(loadedCsv)     # Skipping the first row
                    with open(output_file_path, 'a', encoding='utf-8', newline='') as outfile:
                        csvwriter = csv.writer(outfile)
                        csvwriter.writerows(loadedCsv)
            logging.info(f'Merged CSV files for {country}, path -- {output_file_path}')


if __name__ == '__main__':
    cleaned_data = {'Malta': 'data/Malta/cleaned_data', 'Cyprus': 'data/Cyprus/cleaned_data'}
    ob = Standardize_data(cleaned_data=cleaned_data)
    ob.generate_standardize_data()
