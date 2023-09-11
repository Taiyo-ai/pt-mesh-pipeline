import pandas as pd
import traceback

from ..utils.bucket import (
    read_csv_from_buffer_bucket,
    push_csv_to_buffer_bucket,
    connect_to_buffer_bucket,
)
from ..utils import load_config_yaml
from ..utils.geocoder import Geocoder


class extract_geocode_IIG:
    def __init__(self, **kwargs):
        self.bucket = connect_to_buffer_bucket()
        self.config = kwargs.get("config")
        self.dataset_path = self.config["path_config"]
        self.raw_data = read_csv_from_buffer_bucket(
            self.bucket, self.dataset_path["cleaned_data_path"]
        )
        self.cleaned_data = pd.DataFrame()
        self.raw_data["location"].fillna("", inplace=True)
        self.bucket = connect_to_buffer_bucket()

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

    def save_data(self, df, save_path):
        try:
            push_csv_to_buffer_bucket(self.bucket, df, save_path)
        except Exception as e:
            print(f"Unable to save data to bucket: {e}", traceback.format_exc())

    def run(self):
        try:
            self.cleaned_data = self.extract_geo_detail()
            self.cleaned_data.drop(columns=["label"], inplace=True)
        except Exception as e:
            print(f"Error cleaning data:{e}\n")
        finally:
            self.cleaned_data.to_csv("iig_geo.csv")
        #     self.save_data(
        #         self.cleaned_data,
        #         self.dataset_path["geocoded_data_path"],
        #     )


if __name__ == "__main__":
    path_config = load_config_yaml()["paths"]["IIG"]
    config = {"path_config": path_config}
    geomapper = extract_geocode_IIG(config=config)
    geomapper.run()
