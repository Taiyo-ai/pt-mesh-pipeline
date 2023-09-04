import requests
from bs4 import BeautifulSoup

def scrape_world_bank_data():
    url = "https://ieg.worldbankgroup.org/data"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the HTTP request fails
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract metadata (if available)
        metadata = extract_metadata(soup)

        # Extract raw data (if available)
        raw_data = extract_raw_data(soup)

        return metadata, raw_data
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch data from the website: {str(e)}")
        return None, None

def extract_metadata(soup):
    # Replace this with your logic to extract metadata from the website
    metadata = {
        "source": "World Bank",
        "version": "1.0",
        "timestamp": "2023-09-10"
    }
    return metadata

def extract_raw_data(soup):
    # Replace this with your logic to extract raw data from the website
    raw_data = []
    # Example: Extracting tender names and details
    tender_elements = soup.find_all("h3", class_="Content Type : Reports title")
    for tender in tender_elements:
        name = tender.get_text().strip()
        details = tender.find_next("span", class_="trimmed").get_text().strip()
        raw_data.append({"Tender Name": name, "Tender Details": details})
    return raw_data

   
