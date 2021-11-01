import sys
%pip install pycountry
import pandas as pd
#sys.path.insert(0, 'dummy-data-product/src/dependencies/scraping/')
#import scraper

from scraping import scraper
data = scraper.scrape()

# renaming column names as given
data = data.rename(columns={'Name':'name','Status':'status','Date':'timestamps','Sector':'sector','Country':'country'})

#Mapping status

data.loc[data['status'] == 'Approved', 'status'] = 'Active'
data.loc[data['status'] == 'Archived', 'status'] = 'Closed'
data.loc[data['status'] == 'Dropped', 'status'] = 'Cancelled'
data.loc[data['status'] == 'Terminated', 'status'] = 'Cancelled'

#changing timestamps column to datetime format
data['timestamps'] = pd.to_datetime(data['timestamps'])
