from scrapper import Scrapper
import pandas as pd
from result import results

urls = ['https://etenders.gov.in/eprocure/app',
        'https://www.cpppc.org/en/PPPyd.jhtml',
        'http://www.ggzy.gov.cn/']

if __name__ == '__main__':

    resultss = []

    resultss.append([results(url) for url in urls])

    df=pd.DataFrame(resultss)

    #to save a CSV file
    df.to_csv('ScrapedDataCombined.csv', index=False)

    print(resultss)