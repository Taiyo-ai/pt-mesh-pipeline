# Remove duplicate
import pandas as pd
def duplicate():
    df = pd.read_csv('Data(with Duplications).csv',encoding='cp1252').drop_duplicates('Title',keep='first')
    df.to_csv('Final_Data.csv', index=False)
