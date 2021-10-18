#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 15:11:34 2021

@author: fearless
"""


import pandas as pd







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
#     def strip_data(self,data):
#         data= str(data)
#         data= data[data.find('-')+1:].lstrip(" ")
#         
#     def stripping_column(self):
#         dataframe=self.dataframe
#         column_list=['type_of_buyer','type_of_contract','type_of_procedure','notice_type','regulation','type_of_bid','award_criteria']
#         for column_name in column_list:
#             dataframe[column_name]=dataframe[column_name].apply(self.strip_data)
#             
#         return dataframe
#         
# =============================================================================
        
            

# =============================================================================
# extension = 'csv'
# all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
# 
# #combine all files in the list
# combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
# #export to csv
# combined_csv.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')
# =============================================================================

