from bs4 import BeautifulSoup
import requests
import pandas as pd

class Scrapper:
    r = requests.get('https://etenders.gov.in/eprocure/app')
    html = r.text
    data = BeautifulSoup(html, 'html.parser')

    Tender_Title = []
    Reference_No = []
    Closing_Date = []
    Bid_Opening_Date = []

    tender_even = data.find_all(class_ = 'even')
    tender_odd = data.find_all(class_ = 'odd')


    for i in range(len(tender_even)):
        details = tender_even[i].text.split('\n')
        Tender_Title.append(details[1].split('. ')[-1].strip())
        Reference_No.append(details[2])
        Closing_Date.append(details[3])
        Bid_Opening_Date.append(details[4])

    for i in range(len(tender_odd)):
        details = tender_odd[i].text.split('\n')
        Tender_Title.append(details[1].split('. ')[-1].strip())
        Reference_No.append(details[2])
        Closing_Date.append(details[3])
        Bid_Opening_Date.append(details[4])

    k = {}
    k['Tender_Title'] = Tender_Title
    k['Reference_No'] = Reference_No
    k['Closing_Date'] = Closing_Date
    k['Bid_Opening_Date'] = Bid_Opening_Date

    df = pd.DataFrame(k)


Scrap = Scrapper()
Scrap.df.to_csv('Scrapper_taiyo.csv',index = False)
print(pd.read_csv('Scrapper_taiyo.csv'))



