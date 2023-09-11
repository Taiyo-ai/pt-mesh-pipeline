import pandas as pd
import numpy as np

from ..utils.bucket import (
    connect_to_buffer_bucket,
    read_csv_from_buffer_bucket,
    push_csv_to_buffer_bucket,
)
from ..utils import load_config_yaml
from ..utils.geocoder import Geocoder


class extract_geocode_IIG_Assets:
    def __init__(self):
        self.bucket = connect_to_buffer_bucket()
        self.config = load_config_yaml()
        self.dataset_path = self.config["paths"]["IIG_Assets"]
        self.raw_data = read_csv_from_buffer_bucket(
            self.bucket, self.dataset_path["cleaned_data_path"]
        )
        self.raw_data["location"].fillna("", inplace=True)
        self.cleaned_data = pd.DataFrame()

    def save_data(self, cleaned_data, save_2_path):
        try:
            # if not os.path.exists(save_2_path.split('/')[0]):
            #     os.makedirs(save_2_path.split('/')[0])
            push_csv_to_buffer_bucket(self.bucket, cleaned_data, save_2_path)
            # cleaned_data.to_csv(save_2_path, header=True, index=False)
        except Exception as e:
            print(f"Error saving data\n{e}\n")

    def extract_geo_detail(self):
        geo = Geocoder()
        self.raw_data = geo.geocode_df(self.raw_data, "location", country=True)
        self.raw_data["map_coordinates"] = self.raw_data["map_coordinates"].apply(
            lambda x: [
                [float(x.split(",")[0]), float(x.split(",")[1])]
                if x is not None
                else [20.5937, 78.9629]
            ]
        )
        return self.raw_data

    def run(self):
        try:
            self.cleaned_data = self.extract_geo_detail()
            self.cleaned_data.drop(columns=["label"], inplace=True)
        except Exception as e:
            print(f"Error cleaning data:{e}\n")
        finally:
            self.save_data(self.cleaned_data, self.dataset_path["geocoded_data_path"])


if __name__ == "__main__":
    geo = extract_geocode_IIG_Assets()
    geo.run()
