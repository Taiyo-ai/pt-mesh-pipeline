import warnings
import traceback
import pandas as pd
import numpy as np
import os

warnings.simplefilter(action="ignore")

from .standardizer import generate_raw_text, sector_sub_sector_update

from ..utils import load_config_yaml
from ..utils.bucket import (
    connect_to_buffer_bucket,
    push_csv_to_buffer_bucket,
    read_csv_from_buffer_bucket,
)

from ..utils.metadata import Metadata


class IIGCSRStandardiser:
    def __init__(self, **kwargs):
        self.config: dict = kwargs.get("config")
        self.bucket = connect_to_buffer_bucket()
        self.standardized_df: pd.core.frame.DataFrame = None
        self.metadata = Metadata(name="iig_csr", bucket="taiyo-projects", aws=False)

    def rename_columns(self, df: pd.DataFrame):
        renaming_dict = {
            "description": "description",
            "project_id": "original_id",
            "url": "url",
            "sector": "sector",
            "location": "location",
            "funding_requirement": "budget",
            "funding_details": "funding_details",
            "project_name": "project_name",
            "last_updated": "last_updated_date",
            "subsector": "subsector",
            "data_source": "source",
            "country_name": "country_name",
            "country_code": "country_code",
            "region_name": "region_name",
            "region_code": "region_code",
            "aug_id": "aug_id",
            "project_or_tender": "project_or_tender",
            "map_coordinates": "map_coordinates",
        }

        return df.rename(columns=renaming_dict)

    def standardise_data(self, df):
        try:
            for col in self.config["columns"]:
                df[col] = df[col].replace([np.nan], "")

            df["industry_info"] = df[self.config["columns"]].apply(
                lambda x: " ".join(x.tolist()), axis=1
            )
            df = sector_sub_sector_update(df, "industry_info")

            df["identified_sector"] = df["identified_sector"].apply(
                lambda x: x[0] if len(x) >= 1 else "other"
            )
            df["identified_subsector"] = df["identified_subsector"].apply(
                lambda x: x[0] if len(x) >= 1 else "other"
            )
            df["identified_status"] = "Active"
            # df.drop(columns=["identified_sector_subsector_tuple"], inplace=True)
            return df
        except Exception as e:
            print(f"Error standardising data: {e}", traceback.format_exc())

    def generate_metadata(self):
        try:
            old_standardized_df = read_csv_from_buffer_bucket(
                self.bucket, self.config["standardized_data_path"]
            )
            old_row_count = len(old_standardized_df.index)
        except Exception as e:
            old_row_count = 0

        new_row_count = len(self.standardized_df.index)
        df = pd.DataFrame()
        df["last_updated_date"] = self.standardized_df["last_updated_date"]
        df["last_updated_date"] = df[df["last_updated_date"].notna()]

        df = df.dropna()
        timestamp_range = pd.to_datetime(df["last_updated_date"].astype("str")).dt.date

        self.metadata.create_structure()

        self.metadata.create_metadata(
            df=self.standardized_df,
            source="National Infrastructure Pipline-IIG",
            source_abbr="IIG",
            sector=self.standardized_df["sector"].unique().tolist(),
            subsector=self.standardized_df["subsector"].unique().tolist(),
            source_tags=[],
            country_codes=self.standardized_df["country_code"].unique().tolist(),
            frequency="monthly",
            dataset_type="P",
            indicatorfile="indicators_iig_csr.json",
            datasetfile=self.config["standardized_data_path"],
            timestamp_coverage=[str(timestamp_range.min()), str(timestamp_range.max())],
            no_of_proj_tenders=new_row_count,
            no_of_new_proj_tenders=(new_row_count - old_row_count),
        )

    def load_data(self):
        try:
            df = read_csv_from_buffer_bucket(
                self.bucket, self.config["geocoded_data_path"]
            )
            return df
        except FileNotFoundError as e:
            print(f"Unable to read file from bucket: {e}", traceback.format_exc())

    def save_data(self, df, save_path):
        try:
            push_csv_to_buffer_bucket(self.bucket, df, save_path)
        except Exception as e:
            print(f"Unable to save data to bucket: {e}", traceback.format_exc())

    def run(self):
        try:
            cleaned_data = self.load_data()
            cleaned_data = generate_raw_text(cleaned_data, self.config["columns"])
            cleaned_data = cleaned_data.rename(columns={"sub_sector.1": "subsector"})
            self.standardized_df = self.standardise_data(cleaned_data)
            self.standardized_df = generate_raw_text(
                self.standardized_df, self.config["columns"]
            )
            self.standardized_df = self.rename_columns(self.standardized_df)
            self.generate_metadata()

            self.standardized_df["sector"] = self.standardized_df["sector"].replace(
                np.nan, ""
            )
            self.standardized_df["subsector"] = self.standardized_df[
                "subsector"
            ].replace(np.nan, "")
            self.standardized_df["sector"] = self.standardized_df["sector"].apply(
                lambda x: [] if x == "" else [x]
            )
            self.standardized_df["subsector"] = self.standardized_df["subsector"].apply(
                lambda x: [] if x == "" else [x]
            )
        except Exception as e:
            print(f"Unable to geocode data: {e}", traceback.print_exc())
        finally:
            self.bucket.upload_file(
                filename=os.path.join(self.metadata.base_folder, "metadata.json"),
                key=self.config["metadata_path"],
            )
            # self.standardised_df.to_csv("iig_csr_standard.csv")
            self.save_data(self.standardized_df, self.config["standardized_data_path"])


if __name__ == "__main__":
    path_config = load_config_yaml()["paths"]["IIG_CSR"]
    config = {
        "columns": [
            "sector",
            "subsector",
            "description",
            "project_name",
            "funding_details",
        ],
        "geocoded_data_path": path_config["geocoded_data_path"],
        "standardized_data_path": path_config["standardized_data_path"],
    }
    standardizer = IIGCSRStandardiser(config=config)
    standardizer.run()
