import pandas as pd
tables = pd.read_html("https://etenders.gov.in/eprocure/app")
#after running the commands to get all the table values, table 12 consists of tenders information
df = tables[12]
#giving column names
df.rename(columns = {0:"Tender Title",1:"Reference No",2:"Closing Date",3:"Bid Opening Date"},inplace = True)
#changing date and time to YYYY-MM-DD HH:MM:SS format
df['Closing Date'] = pd.to_datetime(df['Closing Date'])
df['Closing Date'] = df['Closing Date'].dt.strftime('%Y-%m-%d %H:%M:%S')
df['Bid Opening Date'] = pd.to_datetime(df['Bid Opening Date'])
df['Bid Opening Date'] = df['Bid Opening Date'].dt.strftime('%Y-%m-%d %H:%M:%S')
#saving file to csv
df.to_csv('Tenders.csv')
