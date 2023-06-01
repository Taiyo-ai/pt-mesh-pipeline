
from bs4 import BeautifulSoup
import requests

from datetime import datetime

def extraction_first_table(writer):

    head_value = []
    head_value.append('Url')
    response = requests.get("https://etenders.gov.in/eprocure/app")
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup)
    heading = soup.find('tr', class_="list_header").find_all("td")
    for i in heading:
        head1 = i.text
        head_value.append(head1)
    writer.writerow(head_value)
    heading1 = soup.find('span', id="If_17").find_all("tr")
    for tr in heading1:
        row_value = []
        count = 0
        for td in tr("td"):
            title = ''
            if (count == 0):
                title = td.a.text
                title = title.split('.')[1]
                lin = td.find("a")
                url = lin['href']
                row_value.append(url)
                count += 1
            elif (count == 2 or count == 3):
                # 13-jan-2023  11:00 pm
                title = td.text
                title = datetime.strptime(title, "%d-%b-%Y %I:%M   %p")
                count += 1
            else:
                title = td.text
                count+= 1
            row_value.append(title)
        writer.writerow(row_value)
    heading2 = soup.find('span', id="If_19").find_all("tr")
    for tr in heading2:
        row_value = []
        count = 0
        for td in tr("td"):
            title = ''
            if (count == 0):
                title = td.a.text
                title = title.split('.')[1]
                lin = td.find("a")
                url = lin['href']
                row_value.append(url)
                count += 1
            elif (count == 2 or count == 3):
                # 13-jan-2023  11:00 pm
                title = td.text
                title = datetime.strptime(title, "%d-%b-%Y %I:%M   %p")
                count += 1
            else:
                title = td.text
                count += 1
            row_value.append(title)
        writer.writerow(row_value)
    print("Successfully scraped")


def Scrapper(writer):
    try:
        extraction_first_table(writer)

    except Exception as e:
        print(e)
