from os import name, path
from fredapi import Fred
import os
fred = Fred(api_key='795348edc3b0f46479b0ecba8cd33c70')
import pandas as pd


class MyClass:
    path1={}
    search_key=''
    obs_start=''
    obs_end=''
    
    
    def __init__(self,config):
        self.path1=config
   
   
    def take_input(self):
        self.search_key=input()
        self.obs_start = input()
        self.obs_end = input()
    
    
    def extract(self):
        # fred = Fred(api_key='795348edc3b0f46479b0ecba8cd33c70')
        df =fred.search(self.search_key)
        if df is not None:
            print(df)
            series=input()
            if series in df['id']:
                print('Rates for ',df[df.id==series]['title'])
                data = fred.get_series(series,observation_start=self.obs_start,observation_end=self.obs_end)

                data1=pd.DataFrame(data)
                print(data1)
                data1.to_csv(config['raw_data_path'])
            else:
                print('Enter valid series')

        else:
            print('Reconsider the search')

            
    def clean(self):
        df=pd.read_csv(config['raw_data_path'])
        df.dropna(inplace=True)
        df.columns=['Date','Interest Rates']
        df.to_csv(config['cleaned_data_path'])
        

    def load(self):
        df=pd.read_csv(config['cleaned_data_path'])
        df = df.iloc[: , 1:]
        print(df)




if __name__ == "__main__":
    raw_path = r'C:\Users\Dhyey\Desktop\pt-mesh-pipeline\data/content.csv'
    cleaned_path = r'C:\Users\Dhyey\Desktop\pt-mesh-pipeline\data/cleaned.csv'
    raw_relative = os.path.relpath(raw_path)
    cleaned_relative = os.path.relpath(cleaned_path)

    config = {    
            "raw_data_path": raw_relative,
            "cleaned_data_path":cleaned_relative ,
    }

    obj=MyClass(config=config)
    obj.take_input()
    obj.extract()
    obj.clean()
    obj.load()

