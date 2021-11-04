import sys
import pandas as pd

class standardize:

    def __init__(self, data, **kwargs):
        self.config = kwargs.get("config")
        self.data = data

    def standard(self):
        
        # renaming column names as given
        data = self.data.rename(columns={'Name':'name','Status':'status','Date':'timestamps','Sector':'sector','Country':'country_name'})

        #Mapping status
        data.loc[data['status'] == 'Approved', 'status'] = 'Active'
        data.loc[data['status'] == 'Archived', 'status'] = 'Closed'
        data.loc[data['status'] == 'Dropped', 'status'] = 'Cancelled'
        data.loc[data['status'] == 'Terminated', 'status'] = 'Cancelled'

        #changing timestamps column to datetime format
        data['timestamps'] = pd.to_datetime(data['timestamps'])

        return data

if __name__ == "__main__":
  config = {}
  obj = standardize(data, config = config)
  result = obj.standard()
