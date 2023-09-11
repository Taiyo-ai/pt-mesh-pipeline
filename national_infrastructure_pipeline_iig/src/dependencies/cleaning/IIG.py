import re
import numpy as np
import pandas as pd

from pandas.core.frame import DataFrame

from .BaseCleaner import BaseCleaner


class clean_IIG(BaseCleaner):
    def __init__(self, **kwargs):
        super().__init__()
        self.dataset_path = self.config["paths"]["IIG"]
        self.load_data(self.dataset_path)

    def clean(self, df: DataFrame):
        df.drop_duplicates(subset="url", keep="last", inplace=True)

        df.rename(
            columns={
                "country": "country_name",
                "project_title": "project_name",
                "address": "location",
            },
            inplace=True,
        )

        df = df.replace(np.nan, "", regex=True)
        df = df.replace("-", "", regex=True)

        df["data_source"] = "IIG"
        df["country_code"] = "IND"

        df["amount"] = df["investment_in_usd"].apply(
            lambda x: [float(s) for s in re.findall(r"-?\d+\.?\d*", x)][0]
            if [float(s) for s in re.findall(r"-?\d+\.?\d*", x)]
            else ""
        )

        df["multiplier"] = df["investment_in_usd"].apply(
            lambda x: 1000000.0
            if "mn" in str(x)
            else 1000000000.0
            if "bn" in str(x)
            else 1.0
        )

        for i, row in df.iterrows():
            if row["amount"] != "":
                converted_amount = float(row["amount"]) * row["multiplier"]
                df.at[i, "investment_in_usd"] = converted_amount
            else:
                df.at[i, "investment_in_usd"] = ""

        df["region_name"] = df["country_code"].apply(
            lambda x: self.country_code2region_name_dict[x]
            if self.country_code2region_name_dict.keys()
            else x
        )
        df["region_code"] = df["region_name"].apply(
            lambda x: self.region_name2code_dict[x]
            if self.region_name2code_dict.keys()
            else x
        )

        df["location"] = df["location"].replace(
            "Presence Across Nation", "India", regex=True
        )
        df["state"] = df["state"].replace("Presence Across Nation", "", regex=True)

        df["project_id"].apply(lambda x: str(int(x)))
        df["aug_id"] = "IIG_" + df["project_id"].astype(str)
        df["project_or_tender"] = "P"

        df = df.drop(
            [
                "amount",
                "multiplier",
            ],
            axis=1,
        )
        date_columns = [
            "project_start_date",
            "last_updated_date",
            "project_completion_date",
        ]
        df[date_columns] = df[date_columns].apply(pd.to_datetime, errors="coerce")
        df.columns = [i.replace(" ", "_").lower() for i in df.columns.tolist()]
        return df

    def run(self):
        try:
            self.cleaned_data = self.clean(self.raw_data)
            self.cleaned_data.to_csv("iig_clean.csv", index=False)
        except Exception as e:
            print(f"Error cleaning data:{e}\n")
        finally:
            self.save_data(self.cleaned_data, self.dataset_path["cleaned_data_path"])


if __name__ == "__main__":
    clean_IIG().run()
