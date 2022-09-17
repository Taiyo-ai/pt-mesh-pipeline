import os
import re
import numpy as np
import pandas as pd
import hashlib

from pandas.core.frame import DataFrame

from .BaseCleaner import BaseCleaner


class clean_IIG(BaseCleaner):
    def __init__(self, **kwargs):
        super().__init__()
        self.dataset_path = self.config["paths"]["IIG_CSR"]
        self.load_data(self.dataset_path)

    def clean(self, df: DataFrame):
        try:
            df.drop_duplicates(subset="url", keep="last", inplace=True)
            df = df.drop(["project_name", "sub sector"], axis=1)

            df.rename(
                columns={
                    "project_title": "project_name",
                },
                inplace=True,
            )

            df = df.replace(np.nan, "", regex=True)
            df = df.replace("-", "")

            df["data_source"] = "IIG"
            df["country_name"] = "India"
            df["country_code"] = "IND"

            df["multiplier"] = df["funding_requirement"].apply(
                lambda x: 1000000.0
                if "mn" in str(x)
                else 1000000000.0
                if "bn" in str(x)
                else 1.0
            )

            df["funding_requirement"] = df["funding_requirement"].replace(
                ",", "", regex=True
            )
            df["funding_requirement"] = df["funding_requirement"].apply(
                lambda x: [float(s) for s in re.findall(r"-?\d+\.?\d*", x)][0]
                if [float(s) for s in re.findall(r"-?\d+\.?\d*", x)]
                else ""
            )

            for i, row in df.iterrows():
                if row["funding_requirement"] != "":
                    converted_amount = (
                        float(row["funding_requirement"]) * row["multiplier"]
                    )
                    df.at[i, "funding_requirement"] = converted_amount
                else:
                    print("Empty")

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

            df["project_id"] = df["project_id"].apply(lambda x: str(int(x)))
            df["Aug_ID"] = "IIG_" + df["project_id"]
            df["project_or_tender"] = "P"

            df = df.drop(
                [
                    "multiplier",
                ],
                axis=1,
            )

            date_columns = [
                "last_updated",
            ]
            df[date_columns] = df[date_columns].apply(pd.to_datetime, errors="coerce")

            df.columns = [
                i.replace(" ", "_").replace("-", "").lower()
                for i in df.columns.tolist()
            ]
            return df

        except Exception as e:
            print(f"Error cleaning column:\n{e}\n")

    def run(self):

        try:
            self.cleaned_data = self.clean(self.raw_data)
        except Exception as e:
            print(f"Error cleaning data:{e}\n")
        finally:
            self.save_data(self.cleaned_data, self.dataset_path["cleaned_data_path"])
            self.cleaned_data.to_csv("iig_csr_clean.csv")


if __name__ == "__main__":
    clean_IIG().run()
