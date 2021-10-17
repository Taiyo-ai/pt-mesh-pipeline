#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 15:11:34 2021

@author: fearless
"""

from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import re
import requests
import json
import base64
import time
from geopy.geocoders import Nominatim

import csv
import glob




def data_clean(data):
    data=str(data)
    return data.strip("'[]''")


class Clean :
    
    def __init__(self,dataframe):
        self.dataframe=dataframe
    

    
    def finding_duplicates(self):
        dataframe=self.dataframe
        try:
            dataframe = dataframe.drop_duplicates(subset='doc_id', keep="first")
            return dataframe
            
        except Exception:
            pass
            
        finally:
            return dataframe
            

# =============================================================================
# extension = 'csv'
# all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
# 
# #combine all files in the list
# combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
# #export to csv
# combined_csv.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')
# =============================================================================

