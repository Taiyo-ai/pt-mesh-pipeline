import pandas as pd

data = pd.read_csv('scrape.csv')
data = data.drop(['Unnamed: 0', '2'], axis=1)
data.columns = ['Date', 'Notice_title', 'Reference_no.', 'OCID', 'Published_by', 'Deadline_date', 'Notice_type', 'Url']
columns = ['Reference_no.', 'OCID', 'Published_by', 'Deadline_date', 'Notice_type']
for col in columns:
    data[col] = data[col].str.split(':').str[1]
data.to_csv('Final_data.csv')