# import your dependencies here

import pandas as pd

class Stadardization:
    def __init__(self, **kwargs):
        self.csvfile = kwargs.get("csvfile")
        self.df = None
        self.output_file = 'standarize_' + self.csvfile
        # read data from csv
        self.df = pd.read_csv("../../data/" + self.csvfile , encoding='utf-16', delimiter='\t')

    def snake_case(self):
        header_snake_case = [field.lower().replace(' ', '_').replace('/', '_') for field in self.df.columns]
        self.df.columns = header_snake_case

    def saving(self):
        self.df.to_csv('../../data/' + self.output_file, encoding='utf-16' , sep='\t', index=False)

    def run(self):
        print('snake case started...')
        self.snake_case()
        self.saving()
