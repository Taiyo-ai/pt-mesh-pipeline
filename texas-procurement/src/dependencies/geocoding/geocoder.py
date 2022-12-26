import pandas as pd
import logging
import http.client
import urllib.parse
import json
import os
from dependencies.utils import get_path, get_county_location_data


def get_county_location(county):
    conn = http.client.HTTPConnection('api.positionstack.com')

    params = urllib.parse.urlencode({
        'access_key': os.getenv("POSITION_STACK_API_KEY"),
        'query': county,
        'region': 'Texas',
        'limit': 1,
        'country': 'US',
    })

    conn.request('GET', '/v1/forward?{}'.format(params))

    res = conn.getresponse()
    data = res.read()

    return json.loads(data)["data"][0]


class TexasGeocoder:

    def __init__(self) -> None:
        self.df = None
        self.county_location_data = get_county_location_data()

    def load_data(self):
        self.df = pd.read_csv(get_path("cleaned_data_path"), keep_default_na=False, index_col=0)

    def convert_to_map_coordinates(self, x):
        try:
            location = self.county_location_data[x]
        except KeyError:
            location = get_county_location(x)

        latitude = location["latitude"]
        longitude = location["longitude"]

        try:
            return {
                "tyep": "Point",
                "coordinates": [longitude, latitude]
            }
        except Exception as e:
            logging.error(f"{x} not found, ", e)
            return ""

    def process(self):
        self.df["map_coordinates"] = ""
        self.df["County"] = self.df["County"].apply(lambda x: str(x))
        self.df["map_coordinates"] = self.df["County"].apply(lambda x: self.convert_to_map_coordinates(x))

    def save_data(self):
        self.df.to_csv(get_path("geocoded_data_path"))

    def run(self):
        logging.info("Geocoding Started")
        # logging.info(os.getenv("POSITION_STACK_API_KEY"))
        self.load_data()
        self.process()
        self.save_data()
        logging.info("Geocoding Done")


if __name__ == "__main__":
    # Example configuration dictionary
    config = {
        # class specific configuration
        "webdriver_path": "path_to_webdriver",
        "PROCESSES": 15,

        # path configurations
        "path_config": {
            "meta_data_path": "rel_path",
            "raw_data_path": "rel_path",
            "cleaned_data_path": "rel_path",
            "geocoded_data_path": "rel_path",
            "standardized_data_path": "rel_path",
        }
    }
    obj = TexasGeocoder(config=config)
    obj.run()
