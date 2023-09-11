import requests
import pandas as pd
import traceback
import multiprocessing
from multiprocessing import Pool

import warnings

warnings.simplefilter(action="ignore")


class Geocoder:
    def __init__(self, api_key: str = None):
        self.unidentified_locations_ = []
        self.unidentified_coords_ = []
        self.geocoder_dict = None
        self.retry = 5
        self.api_key = api_key

    def geocode(self, location: str, country=False):
        retry = 0
        success = False
        while not success:
            try:
                BASE_URL = f"https://positionstack.com/geo_api.php?query={location}"
                resp = requests.get(BASE_URL).json()
                resp = resp["data"][0]
                if resp != []:
                    json_l = {
                        "query": location,
                        "name": resp["name"],
                        "label": resp["label"],
                        "country": resp["country"],
                        "country_code": resp["country_code"],
                        "state": resp["region"],
                        "map_coordinates": f"{resp['latitude']},{resp['longitude']}",
                        "county": resp["county"],
                        "locality": resp["locality"],
                        "neighbourhood": resp["neighbourhood"],
                    }
                    success = True
                    return json_l
            except Exception as e:
                retry = retry + 1
                print(f"Retry = {retry}\nError encountered: {e}")
                location = " ".join(location.split(" ")[1:])
                print(f'Trying to geocode "{location}"')
                if retry == self.retry:
                    print(f'Error: Unable to geocode the string\n"{location}"')
                    return {}
                    break

    def reverse_geocode(self, map_coordinates):
        retry = 0
        success = False
        YOUR_ACCESS_KEY = self.api_key
        BASE_URL = f"http://api.positionstack.com/v1/reverse?access_key={YOUR_ACCESS_KEY}&query={map_coordinates}"
        while not success:
            try:
                resp = requests.get(BASE_URL).json()
                resp = resp["data"][0]
                if resp != []:
                    json_l = {
                        "query": map_coordinates,
                        "name": resp["name"],
                        "label": resp["label"],
                        "country": resp["country"],
                        "country_code": resp["country_code"],
                        "county": resp["county"],
                        "state": resp["region"],
                        "map_coordinates": f"{resp['latitude']},{resp['longitude']}",
                        "locality": resp["locality"],
                        "neighbourhood": resp["neighbourhood"],
                        "postal_code": resp["postal_code"],
                    }
                    success = True
                    return json_l
            except Exception as e:
                retry = retry + 1
                print(f"Retry = {retry}\nError encountered: {e}")
                if retry == self.retry:
                    print(
                        f'Error: Unable to reverse geocode the string\n"{map_coordinates}"'
                    )
                    return {}
                    break

    def geocode_keys(self, location: str):
        dictionary = {}
        BASE_URL = f"https://positionstack.com/geo_api.php?query={location}"
        retry = 0
        success = False
        while not success:
            try:
                resp = requests.get(BASE_URL).json()
                resp = resp["data"][0]
                if resp != []:
                    json_l = {
                        "query": location,
                        "name": resp["name"],
                        "label": resp["label"],
                        "country": resp["country"],
                        "country_code": resp["country_code"],
                        "state": resp["region"],
                        "map_coordinates": f"{resp['latitude']},{resp['longitude']}",
                        "county": resp["county"],
                        "locality": resp["locality"],
                        "neighbourhood": resp["neighbourhood"],
                    }
                    dictionary[location] = json_l
                    success = True
                    return dictionary

            except Exception as e:
                retry = retry + 1
                print(f"Retry = {retry}\nError encountered: {e}")
                location = " ".join(location.split(" ")[1:])
                print(f'Trying to geocode "{location}"')
                if retry == self.retry:
                    print(f'Error: Unable to geocode the string\n"{location}"')
                    return {}
                    break

    def reverse_geocode_keys(self, map_coordinates):
        dictionary = {}
        retry = 0
        success = False
        YOUR_ACCESS_KEY = self.api_key
        BASE_URL = f"http://api.positionstack.com/v1/reverse?access_key={YOUR_ACCESS_KEY}&query={map_coordinates}"
        while not success:
            try:
                resp = requests.get(BASE_URL).json()
                resp = resp["data"][0]
                if resp != []:
                    json_l = {
                        "query": map_coordinates,
                        "name": resp["name"],
                        "label": resp["label"],
                        "country": resp["country"],
                        "country_code": resp["country_code"],
                        "county": resp["county"],
                        "state": resp["region"],
                        "map_coordinates": f"{resp['latitude']},{resp['longitude']}",
                        "locality": resp["locality"],
                        "neighbourhood": resp["neighbourhood"],
                        "postal_code": resp["postal_code"],
                    }
                    dictionary[map_coordinates] = json_l
                    success = True
                    return dictionary
            except Exception as e:
                retry = retry + 1
                print(f"Retry = {retry}\nError encountered: {e}")
                if retry == self.retry:
                    print(
                        f'Error: Unable to reverse geocode the string\n"{map_coordinates}"'
                    )
                    return {}
                    break

    def generate_unique_locations_dictionary(
        self, df: pd.core.frame.DataFrame, column: str
    ):
        locations = df[column].dropna().unique().tolist()
        print(f"{len(locations)} unique locations found.")
        try:
            geocoder_dict = {}

            pool = Pool(processes=multiprocessing.cpu_count() * 2)
            final_result = pool.map(self.geocode_keys, locations)
            for i in final_result:
                try:
                    if list(i.values())[0]["country_code"] is not None:
                        geocoder_dict[list(i.keys())[0]] = list(i.values())[0]
                    else:
                        self.unidentified_locations_.append(list(i.values())[0])
                except Exception as e:
                    self.unidentified_locations_.append(i)
                    pass

            print("Total geocoded locations =", len(geocoder_dict))
            return geocoder_dict

        except Exception as e:
            print("Error trace:\n", traceback.print_exc())

    def generate_unique_coords_dictionary(self, df: pd.DataFrame, column: str):
        coords = df[column].dropna().unique().tolist()
        print(f"{len(coords)} unique locations found.")
        try:
            geocoder_dict = {}

            pool = Pool(processes=min(df.shape[1], multiprocessing.cpu_count() * 2))
            final_result = pool.map(self.reverse_geocode_keys, coords)
            for i in final_result:
                try:
                    if list(i.values())[0]["country_code"] is not None:
                        geocoder_dict[list(i.keys())[0]] = list(i.values())[0]
                    else:
                        self.unidentified_coords_.append(list(i.values())[0])
                except Exception as e:
                    self.unidentified_coords_.append(i)

            print("Total geocoded locations =", len(geocoder_dict))
            pool.close()  # no more tasks
            pool.join()  # wrap up current tasks
            return geocoder_dict

        except Exception as e:
            print("Error trace:\n", traceback.print_exc())

    def geocode_df(
        self,
        df: pd.core.frame.DataFrame,
        column: str,
        country=False,
        only_map_coords=True,
    ):
        self.geocoder_dict = self.generate_unique_locations_dictionary(df, column)

        try:
            if only_map_coords:
                df["label"] = df[column].apply(
                    lambda x: self.geocoder_dict[x]["label"]
                    if x in self.geocoder_dict.keys()
                    else None
                )
                df["map_coordinates"] = df[column].apply(
                    lambda x: self.geocoder_dict[x]["map_coordinates"]
                    if x in self.geocoder_dict.keys()
                    else None
                )
                df["__country_code"] = df[column].apply(
                    lambda x: self.geocoder_dict[x]["country_code"]
                    if x in self.geocoder_dict.keys()
                    else None
                )
            else:
                df["label"] = df[column].apply(
                    lambda x: self.geocoder_dict[x]["label"]
                    if x in self.geocoder_dict.keys()
                    else None
                )
                if country:
                    df["country"] = df[column].apply(
                        lambda x: self.geocoder_dict[x]["country"]
                        if x in self.geocoder_dict.keys()
                        else None
                    )
                    df["country_code"] = df[column].apply(
                        lambda x: self.geocoder_dict[x]["country_code"]
                        if x in self.geocoder_dict.keys()
                        else None
                    )
                    df["__country_code"] = df[column].apply(
                        lambda x: self.geocoder_dict[x]["country_code"]
                        if x in self.geocoder_dict.keys()
                        else None
                    )
                df["state"] = df[column].apply(
                    lambda x: self.geocoder_dict[x]["state"]
                    if x in self.geocoder_dict.keys()
                    else None
                )
                df["county"] = df[column].apply(
                    lambda x: self.geocoder_dict[x]["county"]
                    if x in self.geocoder_dict.keys()
                    else None
                )
                df["locality"] = df[column].apply(
                    lambda x: self.geocoder_dict[x]["locality"]
                    if x in self.geocoder_dict.keys()
                    else None
                )
                df["neighbourhood"] = df[column].apply(
                    lambda x: self.geocoder_dict[x]["neighbourhood"]
                    if x in self.geocoder_dict.keys()
                    else None
                )
                df["map_coordinates"] = df[column].apply(
                    lambda x: self.geocoder_dict[x]["map_coordinates"]
                    if x in self.geocoder_dict.keys()
                    else None
                )
            return df
        except Exception as e:
            print("Error:\n", e)

    def reverse_geocode_df(
        self, df: pd.core.frame.DataFrame, column: str, country=False
    ):
        self.reverse_geocoder_dict = self.generate_unique_coords_dictionary(df, column)

        try:
            df["label"] = df[column].apply(
                lambda x: self.reverse_geocoder_dict[x]["label"]
                if x in self.reverse_geocoder_dict.keys()
                else None
            )
            if country:
                df["country"] = df[column].apply(
                    lambda x: self.reverse_geocoder_dict[x]["country"]
                    if x in self.reverse_geocoder_dict.keys()
                    else None
                )
                df["country_code"] = df[column].apply(
                    lambda x: self.reverse_geocoder_dict[x]["country_code"]
                    if x in self.reverse_geocoder_dict.keys()
                    else None
                )
            df["county"] = df[column].apply(
                lambda x: self.reverse_geocoder_dict[x]["county"]
                if x in self.reverse_geocoder_dict.keys()
                else None
            )
            df["state"] = df[column].apply(
                lambda x: self.reverse_geocoder_dict[x]["state"]
                if x in self.reverse_geocoder_dict.keys()
                else None
            )
            df["neighbourhood"] = df[column].apply(
                lambda x: self.reverse_geocoder_dict[x]["neighbourhood"]
                if x in self.reverse_geocoder_dict.keys()
                else None
            )
            df["locality"] = df[column].apply(
                lambda x: self.reverse_geocoder_dict[x]["locality"]
                if x in self.reverse_geocoder_dict.keys()
                else None
            )
            return df
        except Exception as e:
            print("Error:\n", e)
