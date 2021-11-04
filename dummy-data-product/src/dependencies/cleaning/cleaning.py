import pandas as pd
import numpy as np
import pycountry

class cleaning:

  def __init__(self, data, **kwargs):
    self.config = kwargs.get("config")
    self.data = data
  
  def clean(self):

    #dropping all rows whose source is NaN.
    result = self.data[self.data['source'].notna()]

    #filling all country codes with '000' whose country codes couldn't be scrapped.
    result['country_code'] = result['country_code'].fillna('000')
    result.country_code = result['country_code'].astype(int)
    result['country_code'] = ['%03d' % a for a in result['country_code']]

    #replacing country codes with alpha_3 names
    for i in result['country_code']:
      if i == '000':
        pass
      else:
        result['country_code'] = result['country_code'].replace(i,pycountry.countries.search_fuzzy(str(i))[0].alpha_3)

    #Conversion of budget amounts to USD
    result['budget'] = '$' + result['budget'].astype(str)
    
    return (result)


if __name__ == "__main__":
  config = {}
  obj = cleaning(data, config = config)
  result = obj.clean()
