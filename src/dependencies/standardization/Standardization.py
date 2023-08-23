#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import json
import os

class Standardization:
    def __init__(self):
        with open('./config.json') as file:
            data = json.load(file)
        self.output_name = data['output_csv']
        self.df = pd.read_csv('../data/' + self.output_name, encoding='utf-16', delimiter='\t')
    
    def snake_case(self):
        columns = []
        for column in self.df.columns:
            if '/' in column:
                list1 = column.split('/')
                list1 = [i.strip() for i in list1]
                column = "/".join(list1).replace(" ","_").lower()
            else:
                column = column.replace(" ","_").lower()
            columns.append(column)
        self.df.columns = columns
        
    def saving(self):
        self.df.to_csv('../data/' + self.output_name, encoding='utf-16',sep='\t', index=False)

