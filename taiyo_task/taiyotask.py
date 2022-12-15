from bs4 import BeautifulSoup
import requests
from csv import writer

url = "https://opentender.eu/start"
try:
    source = requests.get(url)
    source.raise_for_status()
    soup = BeautifulSoup(source.content,"html.parser")


    tenders = soup.find("ul",class_="portal-links").find_all("li",class_="portal-link")

    with open("tender_list.csv", "w", encoding="utf8", newline="") as file:
        thewriter = writer(file)
        header = ["Country","Nr. of Tenders"]
        thewriter.writerow(header)

        for tender in tenders:
            country =tender.find("a").text
            nr_of_tenders = tender.find("div").text
            # print(country,nr_of_tenders)
            info = [country,nr_of_tenders]
            thewriter.writerow(info)

except Exception as e:
    print(e)
