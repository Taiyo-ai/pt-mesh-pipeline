import requests
import pandas as pd
import lxml
from bs4 import BeautifulSoup



l = []


class Scrapper:

    def get_data(self):

        base_url = "https://www.contractsfinder.service.gov.uk/Search/Results?&page="
        for page in range(1, 125):  # No. of pages to scan for data, it can be changed
            r = requests.get(base_url + str(page) + "#dashboard_notices.html")
            c = r.content
            soup = BeautifulSoup(c, "lxml")
            all_data = soup.find_all("div", {"class": "search-result"})
            for item in all_data:
                d = {}

                d["Tender"] = item.find("a", {"class": ["govuk-link", "search-result-rwh", "break-word"]}).text

                d["Company"] = item.find("div", {"class": ["search-result-sub-header", "wrap-test"]}).text

                d["Procurement"] = item.find_all("div", {"class": "search-result-entry"})[0].text.replace(
                    "Procurement stage", " ")

                d["Notice"] = item.find_all("div", {"class": "search-result-entry"})[1].text.replace("Notice status",
                                                                                                     " ")

                d["Location"] = item.find_all("div", {"class": "search-result-entry"})[3].text.replace(
                    "Contract location", " ")

                try:
                    d["Closing"] = item.find_all("div", {"class": "search-result-entry"})[2].text.replace("Closing",
                                                                                                          " ")
                except:
                    d["Closing"] = "None"
                try:
                    d["Value"] = item.find_all("div", {"class": "search-result-entry"})[4].text.replace(
                        "Contract value", " ")
                except:
                    d["Value"] = "None"
                try:
                    d["Date"] = item.find_all("div", {"class": "search-result-entry"})[5].text.replace(
                        "Publication date", " ")
                except:
                    d["Date"] = "None"
                l.append(d)
        return



obj=Scrapper()
obj.get_data()

df=pd.DataFrame(l)
print(df.head(5))
df.to_csv("UK_data.csv",index=False)