import pandas as pd
import re

class Standard:
    def __init__(self, data):
        self.data = data
        self.data_clean = pd.read_csv(self.data)

    def rename_columns(self):
        self.data_clean.columns = self.data_clean.columns.str.lower().str.replace(' ', '_')
        return self.data_clean

    def datetime_convert(self):
        date_columns = ["e-Published Date", "Bid Submission Closing Date", "Tender Opening Date"]
        # for col in date_columns:
            # self.data_clean[col] = pd.to_datetime(self.data_clean[col], format='%d-%b-%Y %I:%M %p')
        self.data_clean[date_columns] = self.data_clean[date_columns].apply(pd.to_datetime, format='%d-%b-%Y %I:%M %p')

        return self.data_clean