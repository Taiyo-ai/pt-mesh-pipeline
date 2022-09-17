import pandas as pd
import numpy as np
import warnings
import traceback

warnings.simplefilter(action="ignore")

from .geocoder import Geocoder
from ..utils import load_config_yaml
from ..utils.bucket import (
    connect_to_buffer_bucket,
    push_csv_to_buffer_bucket,
    read_csv_from_buffer_bucket,
)


class EPIGeocoder:
    def __init__(self, api_key: str = None, **kwargs):
        self.config = kwargs.get("config")
        self.bucket = connect_to_buffer_bucket()
        self.api_key: str = api_key
        self.geocoder = Geocoder(self.api_key)
        self.geodf: pd.core.frame.DataFrame = None

    def load_data(self):
        try:
            df = read_csv_from_buffer_bucket(
                self.bucket, self.config["cleaned_data_path"]
            )
            return df
        except FileNotFoundError as e:
            print(f"Unable to read file from bucket: {e}", traceback.format_exc())

    def geocode(self, df):
        df["location"] = df["location"].replace([np.nan], "")
        df["state_name"] = df["state_name"].replace([np.nan], "")
        df["country_name"] = df["country_name"].replace([np.nan], "")
        df["location_col"] = df[["location", "state_name", "country_name"]].apply(
            lambda x: ", ".join(x.tolist()), axis=1
        )

        df = self.geocoder.geocode_df(df, "location_col", only_map_coords=False)
        unindentified_df = df[df["map_coordinates"].isnull()]
        unindentified_df = self.geocoder.geocode_df(unindentified_df, "country_name")
        df = df[~df["map_coordinates"].isnull()]
        df = df.append(unindentified_df, ignore_index=True)
        df.drop(columns=["location_col"], inplace=True)

        df["map_coordinates"] = df["map_coordinates"].apply(
            lambda x: [[round(float(i), 4) for i in x.split(",")]]
        )
        return df

    def save_data(self, df, save_path):
        try:
            push_csv_to_buffer_bucket(self.bucket, df, save_path)
        except Exception as e:
            print(f"Unable to save data to bucket: {e}", traceback.format_exc())

    def run(self):
        try:
            cleaned_data = self.load_data()
            self.geodf = self.geocode(cleaned_data)
        except Exception as e:
            print(f"Unable to geocode data: {e}", traceback.print_exc())
        finally:
            self.save_data(self.geodf, self.config["geocoded_data_path"])


if __name__ == "__main__":
    path_config = load_config_yaml()["paths"]["EPIHVTC"]
    geomapper = EPIGeocoder(config=path_config)
    geomapper.run()
