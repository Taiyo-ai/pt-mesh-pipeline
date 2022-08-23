import requests
import pandas as pd

class super_scraper():
    def scrape():
        url = "https://opentender.eu/api/all/tender/search"

        headers = {
            "authority": "opentender.eu",
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-type": "application/json",
            "origin": "https://opentender.eu",
            "referer": "https://opentender.eu/all/search/tender",
            "sec-ch-ua": "^\^Chromium^^;v=^\^104^^, ^\^",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
            "scheme": "https"
        }

        response = requests.request("POST", url, headers=headers)
        data=response.json()
        total_tenders=data['data']['hits']['total']
        print(total_tenders)


        df=pd.DataFrame()
        tenders=0
        while True:
            if tenders>=total_tenders:
                break

            response = requests.request("POST", url, json={'from':f'{tenders}',"size":"100"},headers=headers)

            data=response.json()

            # print(data['data']['hits']['total'])
            # print(len(data['data']['hits']['hits']))

            res=[]

            for detial in data['data']['hits']['hits']:
                res.append(detial)


            df=df.append(pd.json_normalize(res))
            # print(tenders, ' Tender Found')
            tenders+=100
        df.to_csv('data.csv',index=False)


if __name__=='__main__':
    super_scraper.scrape()