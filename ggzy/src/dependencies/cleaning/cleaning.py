import pandas as pd
import logging
import os

class Cleaner():
    
    def run(self):
        logging.info("Cleaning Main Data")
        
        os.chdir("../../")
        folder_path = os.getcwd()
        file_path = os.path.join(folder_path + "\data", "raw_data.csv")

        df = pd.read_csv(file_path)

        df.drop_duplicates(inplace = True)

        file_path = os.path.join(folder_path + "\data", "cleaned_data.csv")
        
        del df['tradeShow']
        del df['titleShow']
        
        df.fillna("NA", inplace = True)
        
        df = df.rename(columns={'title': 'name', 'stageShow': 'status', 'timeShow': 'open_date', 'platformName': 'platform_name', 'classifyShow': 'classify_show', 'districtShow': 'location', 'stageName': 'stage_name'})
        
        df.to_csv(file_path, index=False)