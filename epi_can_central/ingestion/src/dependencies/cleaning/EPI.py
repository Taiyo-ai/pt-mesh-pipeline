import numpy as np
import pandas as pd

from datetime import datetime

from .BaseCleaner import BaseCleaner


class clean_EPI(BaseCleaner):
    def __init__(self, **kwargs):
        super().__init__()
        self.extra_config = kwargs.get("extra_config")
        self.dataset_path = self.config["paths"][self.extra_config["source_abbr"]]
        for key in list(self.dataset_path.keys()):
            self.dataset_path[key] = self.dataset_path[key].replace(
                "<year>", self.extra_config["year"]
            )
        self.load_data(self.dataset_path)

    # def get_status(self, X):
    #     if X >= pd.to_datetime(datetime.today(), errors="coerce"):
    #         return "Active"
    #     else:
    #         return "Closed"

    def clean(self, df):
        try:
            df["title"] = df["title"].apply(str.title)
            df["location"] = df["location"].apply(str.title)
            try:
                df["state_name"] = df["state_name"].astype("string")
                df["state_name"] = df["state_name"].apply(str.title)
            except Exception as e:
                print("Column not found: state_name")
                pass
            df["inviting_authority_name"] = df["inviting_authority_name"].apply(
                str.title
            )
            df["inviting_authority_address"] = df["inviting_authority_address"].apply(
                str.title
            )
            df["work_description"] = df["work_description"].apply(str.title)

            df["epublished_date"] = pd.to_datetime(
                df["epublished_date"], errors="coerce"
            )
            df["epublished_date_"] = pd.to_datetime(
                df["epublished_date_"], errors="coerce"
            )
            df["tender_opening_date"] = pd.to_datetime(
                df["tender_opening_date"], errors="coerce"
            )
            df["bid_opening_date"] = pd.to_datetime(
                df["bid_opening_date"], errors="coerce"
            )
            df["bid_submission_start_date"] = pd.to_datetime(
                df["bid_submission_start_date"], errors="coerce"
            )
            df["bid_submission_closing_date"] = pd.to_datetime(
                df["bid_submission_closing_date"], errors="coerce"
            )
            df["bid_submission_end_date"] = pd.to_datetime(
                df["bid_submission_end_date"], errors="coerce"
            )
            df["document_download_start_date"] = pd.to_datetime(
                df["document_download_start_date"], errors="coerce"
            )
            df["document_download_end_date"] = pd.to_datetime(
                df["document_download_end_date"], errors="coerce"
            )
            # df["status"] = df["bid_submission_closing_date"].apply(
            #     lambda x: self.get_status(x)
            # )
            df["status"] = df["status"].apply(str.title)

            df["tender_fee"] = (
                df["tender_fee"]
                .astype(str)
                .apply(lambda x: float(x.replace("₹", "").strip()) * 0.013)
            )
            df["emd"] = (
                df["emd"]
                .astype(str)
                .apply(lambda x: float(x.replace("₹", "").strip()) * 0.013)
            )
            df["budget"] = np.nan

            df["country_name"] = "India"
            df["country_code"] = "IND"

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

            df["source"] = self.extra_config["source_abbr"]
            df["project_or_tender"] = "T"
            df["aug_id"] = f"{self.extra_config['source_abbr']}_" + df[
                "tender_reference_number"
            ].astype(str)
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


if __name__ == "__main__":
    extra_config = {"source_abbr": "EPICANC", "year": "2021"}
    clean_EPI(extra_config=extra_config).run()
