import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def extract_metadata(metadata_url, metadata_csv):
    # Implement logic to extract metadata from a website
    response = requests.get(metadata_url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        metadata = {
            'title': soup.title.string if soup.title else None,
            'description': soup.find('meta', attrs={'name': 'description'})['content'] if soup.find('meta', attrs={'name': 'description'}) else None,
            # Add more metadata fields as needed
        }
        # Save metadata to CSV in the 'data' folder
        data_folder = 'data'
        os.makedirs(data_folder, exist_ok=True)
        metadata_df = pd.DataFrame([metadata])
        metadata_df.to_csv(os.path.join(data_folder, metadata_csv), index=False)
        return metadata
    else:
        return None

def extract_raw_data(raw_data_api_url, raw_data_csv):
    # Implement logic to extract raw data from an API or web service
    response = requests.get(raw_data_api_url)
    if response.status_code == 200:
        if 'application/json' in response.headers.get('content-type', '').lower():
            try:
                raw_data = response.json()  # Try to decode JSON
                # Save raw data to CSV in the 'data' folder
                data_folder = 'data'
                os.makedirs(data_folder, exist_ok=True)
                raw_data_df = pd.DataFrame(raw_data)
                raw_data_df.to_csv(os.path.join(data_folder, raw_data_csv), index=False)
                return raw_data
            except ValueError:
                print("Failed to decode JSON data.")
                return None
        else:
            print("API did not return JSON data.")
            return None
    else:
        return None

# Example usage
if __name__ == "__main__":
    metadata_url = 'https://ieg.worldbankgroup.org/ieg-search?search_api_fulltext=tender&field_topic=All&field_sub_category=All&content_type_1=&field_organization_tags=All&type_2_op=not&type_2%5B%5D=homepage_spotlight_feature&sort_by=search_api_relevance&sort_order=DESC'
    metadata_csv = 'metadata.csv'
    raw_data_api_url = 'https://ieg.worldbankgroup.org/ieg-search?search_api_fulltext=tender&field_topic=All&field_sub_category=All&content_type_1=&field_organization_tags=All&type_2_op=not&type_2%5B%5D=homepage_spotlight_feature&sort_by=search_api_relevance&sort_order=DESC'
    raw_data_csv = 'raw_data.csv'

    metadata = extract_metadata(metadata_url, metadata_csv)
    if metadata:
        print("Metadata:", metadata)

    raw_data = extract_raw_data(raw_data_api_url, raw_data_csv)
    if raw_data:
        print("Raw Data:", raw_data)
