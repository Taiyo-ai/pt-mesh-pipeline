from numpy.lib.function_base import select
import pandas as pd
from geopy.geocoders import Nominatim

from ..utils.bucket import (
    connect_to_buffer_bucket,
    read_csv_from_buffer_bucket,
    push_csv_to_buffer_bucket,
)
from ..utils import load_config_yaml
from ..utils.geocoder import Geocoder


class extract_geocode_IIG_CSR:
    def __init__(self):
        self.bucket = connect_to_buffer_bucket()
        self.config = load_config_yaml()
        self.dataset_path = self.config["paths"]["IIG_CSR"]
        self.raw_data = read_csv_from_buffer_bucket(
            self.bucket, self.dataset_path["cleaned_data_path"]
        )

        self.raw_data["location"].fillna("", inplace=True)

    def save_data(self, cleaned_data, save_2_path):
        try:
            # if not os.path.exists(save_2_path.split('/')[0]):
            #     os.makedirs(save_2_path.split('/')[0])
            push_csv_to_buffer_bucket(self.bucket, cleaned_data, save_2_path)
            # cleaned_data.to_csv(save_2_path, header=True, index=False)
        except Exception as e:
            print(f"Error saving data\n{e}\n")

    def extract_geo_detail(self):
        self.raw_data = self.geocode(self.raw_data)
        return self.raw_data

    def geocode(self, df):

        geolocator = Nominatim(user_agent="geoapiExercises")
        map_coordinates = []
        try:
            for i in range(len(df)):
                map_cor = []
                locations = df["location"][i]
                test_list = locations.replace("[", "").replace("]", "").split("'")
                locations = [test_list[i] for i in range(len(test_list)) if i % 2 != 0]
                for j in range(len(locations)):
                    try:
                        name = locations[j]
                        loc = geolocator.geocode(name)

                        try:
                            lat_long = [loc.latitude, loc.longitude]
                            map_cor.append(lat_long)
                        except Exception as e:
                            pass
                    except Exception as e:
                        print(f"Error cleaning data:{e}\n")
                map_coordinates.append(map_cor)
            df["map_coordinates"] = map_coordinates

        except Exception as e:
            print(f"Error cleaning data:{e}\n")

        return df

    def run(self):
        try:
            self.cleaned_data = self.extract_geo_detail()
        except Exception as e:
            print(f"Error cleaning data:{e}\n")
        finally:
            self.save_data(self.cleaned_data, self.dataset_path["geocoded_data_path"])
            self.cleaned_data.to_csv("iig_csr_geo.csv")


if __name__ == "__main__":
    geo = extract_geocode_IIG_CSR()
    geo.run()
