import pandas as pd
import numpy as np
import re
from geopy.geocoders import Nominatim
from .BaseCleaner import BaseCleaner


class clean_PPPIndia(BaseCleaner):
    def __init__(self, **kwargs):
        super().__init__()
        self.dataset_path = self.config["paths"]["BOUYGUES"]
        self.load_data(self.dataset_path)

    def convert_amt2usd(self, amt: list):
        for i in range(len(amt)):
            if "INR" in amt[i]:
                amt[i] = re.sub("[INR]", "", amt[i])
                cf = 1.21
                if "million" in amt[i]:
                    amt[i] = float(re.sub("[million]", "", amt[i])) * 1000000 * cf
                elif "billion" in amt[i]:
                    amt[i] = float(re.sub("[billion]", "", amt[i])) * 1000000000 * cf
                else:
                    amt[i] = float(amt[i]) * cf

    def clean(self, df):
        try:
            df["project_cost"] = df["project_cost"].replace([np.nan], "")
            df["project_cost"] = df["project_cost"].apply(
                lambda x: re.findall(
                    r"(?:[A-Z]{3})\d{1,3}(?:,\d{3})+(?:\.\d{2})?|(?:(?:[A-Z]{2,3} )\d+(?:\.\d+)?\s?(?:b|m|tr)illion)",
                    x,
                )
            )
            df["project_cost"] = df["project_cost"].apply(
                lambda x: [i.replace(",", "") for i in x]
            )
            df["project_cost"] = df["project_cost"].apply(
                lambda x: np.nan if len(x) < 1 else x
            )
            df["project_cost"] = df["project_cost"].apply(
                lambda x: self.convert_amt2usd(x) if type(x) == list else np.nan
            )
            df["project_cost"] = df["project_cost"]

            df["project_name"] = df["project_name"].replace(np.nan, "")
            df["sector"] = df["sector"].replace(np.nan, "")
            df["sub_sector"] = df["sub_sector"].replace(np.nan, "")
            df["location"] = df["location"].replace(np.nan, "")
            df["type"] = df["type"].replace(np.nan, "")
            df["status"] = df["status"].replace(np.nan, "")
            df["project_authority"] = df["project_authority"].replace(np.nan, "")
            df["date_of_award"] = df["date_of_award"].replace(np.nan, "")
            df["update_date"] = df["update_date"].replace(np.nan, "")

            df["country"] = "India"
            df["country_code"] = "IND"
            df["project_or_tender"] = "P"
            df["source"] = "PPPINDIA"
            df["aug_id"] = "PPPINDIA_" + df["project_id"]

            geolocator = Nominatim(user_agent="myApp")
            for i in df.index:
                location = geolocator.geocode(df["loctaion"][i])
                df.loc[i, "lat"] = location.latitude
                df.loc[i, "long"] = location.longitude
                df.loc[i, "lat"] = ""
                df.loc[i, "long"] = ""

            return df
        except Exception as e:
            print(f"Error cleaning column:\n{e}\n")

    def run(self):
        try:
            self.cleaned_data = self.clean()
            return self.cleaned_data
        except Exception as e:
            print(f"Error cleaning data:{e}\n")
        finally:
            self.save_data(self.cleaned_data, self.dataset_path["cleaned_data_path"])


def main():
    df = clean_PPPIndia()
    df = df.run()
    return df


if __name__ == "__main__":
    mn = main()
