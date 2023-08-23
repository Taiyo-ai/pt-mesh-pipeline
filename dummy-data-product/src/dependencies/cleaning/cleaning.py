import re
import pandas as pd

class Cleaner:
    def __init__(self, data):
        self.data = data
        self.data_clean = pd.read_csv(self.data)

    def arrange_title_column(self):
        pattern = r'\[(.*?)\]'
        extracted_values = self.data_clean["Title and Ref"].apply(lambda x: re.findall(pattern, x))

        # Create new columns
        self.data_clean["Title"] = extracted_values.str[0]
        self.data_clean["Ref"] = extracted_values.str[1]
        self.data_clean["Tender ID"] = extracted_values.str[2]

        #Drop the original column
        self.data_clean.drop(columns=["Title and Ref"], inplace=True)

        return self.data_clean


    def remove_duplicate_rows(self):
        self.data_clean = self.data_clean.drop_duplicates()
        return self.data_clean

    def remove_rows_with_empty_values(self):
        self.data_clean = self.data_clean.dropna()
        return self.data_clean

