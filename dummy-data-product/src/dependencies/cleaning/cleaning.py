import pandas
import rates

def missing_value_adjustment(x):
    if x.isnan==True:
        x='undefined'

def exchange_currency(value, country):
    exc_rate = rates.set_index(['from_currency', 'to_currency', 'date'])['exc_rate']
    company['converted'] = company.apply(convert_to_usd, axis=1)
    def convert_to_usd(row):
        return row['value'] * exc_rate[row['currency'], 'USD', row['date']]
    

def sector_mapping:

def status_mapping:

def country_code_mapper:
#
