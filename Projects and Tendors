import requests
from bs4 import BeautifulSoup as bs
import pandas as pd


def get_soup(page):
    print(f"Retrieving page: {page}")
    url_parse = f'https://www.contractsfinder.service.gov.uk/Search/Results?&page={page}#dashboard_notices'
    response = requests.get(url_parse)
    soup_attr = bs(response.content, 'html.parser')
    return soup_attr


def generate_basic_dict(contract):
    temp_dict = {}
    title = contract.find('div', class_='search-result-header')['title']
    sub_text = contract.find_all('div', class_="wrap-text")

    temp_dict["Title"] = title
    temp_dict["Sub Title"] = sub_text[0].text
    temp_dict["Tender Description"] = sub_text[1].text
    return temp_dict

final_submission = []
soup = get_soup(1)
max_page = soup.find_all(class_="standard-paginate")
max_value = max_page[-1].text.lstrip()
for page in range(1, int(max_value) + 1):
    if page != 1:
        soup = get_soup(page)
    tenders = soup.find_all(class_="search-result")
    print(f"About to process {len(tenders)} records")
    for tender in tenders:
        final_output = generate_basic_dict(tender)
        contract_attr = tender.find_all('div', {'class': "search-result-entry"})
        for attr in contract_attr:
            key = attr.contents[0].text
            value = attr.contents[1].lstrip()
            final_output[key] = value
        final_submission.append(final_output)
df = pd.DataFrame(final_submission)
df.to_csv('test_scrap.csv', index=False)
