import os
import warnings
import traceback
import pandas as pd
import numpy as np

warnings.simplefilter(action="ignore")

from .standardizer import (
    sector_sub_sector_update,
)
from ..utils import load_config_yaml
from ..utils.bucket import (
    connect_to_buffer_bucket,
    push_csv_to_buffer_bucket,
    read_csv_from_buffer_bucket,
)
from ..utils.metadata import Metadata


class EPIStandardiser:
    def __init__(self, **kwargs):
        self.config: dict = kwargs.get("config")
        self.bucket = connect_to_buffer_bucket()
        self.standardised_df: pd.core.frame.DataFrame = None
        self.metadata = Metadata(name="epihvtc", bucket="taiyo-projects", aws=False)

    def rename_columns(self, df: pd.core.frame.DataFrame):
        renaming_dict = {
            "aug_id": "aug_id",
            "bid_opening_date": "bid_opening_date",
            "bid_submission_closing_date": "bid_submission_closing_date",
            "bid_submission_end_date": "bid_submission_end_date",
            "bid_submission_start_date": "bid_submission_start_date",
            "budget": "budget",
            "corrigendum": "corrigendum",
            "country_code": "country_code",
            "country_name": "country_name",
            "county": "county",
            "document_download_end_date": "document_download_end_date",
            "document_download_start_date": "document_download_start_date",
            "emd": "emd",
            "epublished_date": "epublished_date",
            "epublished_date_": "epublished_date_",
            "inviting_authority_address": "inviting_authority_address",
            "inviting_authority_name": "inviting_authority_name",
            "label": "label",
            "locality": "locality",
            "location": "location",
            "map_coordinates": "map_coordinates",
            "neighbourhood": "neighbourhood",
            "organization_name": "organization_name",
            "organization_type": "organization_type",
            "product_category": "sector",
            "product_sub_category": "subsector",
            "project_or_tender": "project_or_tender",
            "region_code": "region_code",
            "region_name": "region_name",
            "sessioned_url": "sessioned_url",
            "source": "source",
            "state": "state",
            "state_name": "state_name",
            "status": "status",
            "tender_category": "tender_category",
            "tender_document_link": "url",
            "tender_fee": "tender_fee",
            "tender_opening_date": "tender_opening_date",
            "tender_reference_number": "original_id",
            "tender_type": "tender_type",
            "title": "name",
            "work_description": "work_description",
            "identified_status": "identified_status",
            "identified_sector": "identified_sector",
            "identified_subsector": "identified_subsector",
            "identified_sector_subsector_tuple": "identified_sector_subsector_tuple",
        }
        return df.rename(columns=renaming_dict)

    def typecast_df(self, df: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
        df.fillna(np.nan, inplace=True)
        for col in df.columns:
            df[col] = df[col].apply(lambda x: "nan" if x == "" else x)

        df["original_id"] = df["original_id"].astype(str)
        df["aug_id"] = df["aug_id"].astype(str)
        df["source"] = df["source"].astype(str)
        df["name"] = df["name"].astype(str)
        df["status"] = df["status"].astype(str)
        df["project_or_tender"] = df["project_or_tender"].astype(str)

        df["tender_fee"] = df["tender_fee"].astype("float64")
        df["emd"] = df["emd"].astype("float64")
        df["budget"] = df["budget"].astype("float64")

        df["epublished_date"] = df["epublished_date"].astype(str)
        df["epublished_date_"] = df["epublished_date_"].astype(str)
        df["tender_opening_date"] = df["tender_opening_date"].astype(str)
        df["bid_opening_date"] = df["bid_opening_date"].astype(str)
        df["bid_submission_start_date"] = df["bid_submission_start_date"].astype(str)
        df["bid_submission_closing_date"] = df["bid_submission_closing_date"].astype(
            str
        )
        df["bid_submission_end_date"] = df["bid_submission_end_date"].astype(str)
        df["document_download_start_date"] = df["document_download_start_date"].astype(
            str
        )
        df["document_download_end_date"] = df["document_download_end_date"].astype(str)

        df["identified_sector"] = df["identified_sector"].astype(str)
        df["identified_subsector"] = df["identified_subsector"].astype(str)
        df["identified_sector_subsector_tuple"] = df[
            "identified_sector_subsector_tuple"
        ].astype(str)

        df["organization_name"] = df["organization_name"].astype(str)
        df["organization_type"] = df["organization_type"].astype(str)
        df["tender_type"] = df["tender_type"].astype(str)
        df["tender_category"] = df["tender_category"].astype(str)
        df["sector"] = df["sector"].astype(str)
        df["subsector"] = df["subsector"].astype(str)

        df["location"] = df["location"].astype(str)
        df["state_name"] = df["state_name"].astype(str)
        df["work_description"] = df["work_description"].astype(str)
        df["corrigendum"] = df["corrigendum"].astype(str)
        df["inviting_authority_name"] = df["inviting_authority_name"].astype(str)
        df["inviting_authority_address"] = df["inviting_authority_address"].astype(str)
        df["url"] = df["url"].astype(str)
        df["sessioned_url"] = df["sessioned_url"].astype(str)

        df["country_name"] = df["country_name"].astype(str)
        df["country_code"] = df["country_code"].astype(str)
        df["region_name"] = df["region_name"].astype(str)
        df["region_code"] = df["region_code"].astype(str)
        df["label"] = df["label"].astype(str)
        # df["state"] = df["state"].astype(str)
        # df["county"] = df["county"].astype(str)
        # df["locality"] = df["locality"].astype(str)
        # df["neighbourhood"] = df["neighbourhood"].astype(str)
        df["map_coordinates"] = df["map_coordinates"].astype(str)

        return df

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
            df["identified_status"] = (
                df["status"]
                .replace([np.nan], "Not Available")
                .replace({"Active": "Trending", "Closed": "Closed"})
            )
            date_col_list = [
                "epublished_date",
                "epublished_date_",
                "tender_opening_date",
                "bid_opening_date",
                "bid_submission_start_date",
                "bid_submission_closing_date",
                "bid_submission_end_date",
                "document_download_start_date",
                "document_download_end_date",
            ]
            for col in date_col_list:
                df[col] = pd.to_datetime(df[col], errors="coerce").dt.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            df["timestamps"] = df[date_col_list].apply(lambda x: x.to_dict(), axis=1)
            df["timestamp_range"] = df[date_col_list].apply(
                lambda x: {"min": min(x), "max": max(x)}, axis=1
            )
            df = self.rename_columns(df)
            df = self.typecast_df(df)
            return df
        except Exception as e:
            print(f"Error standardising data: {e}", traceback.format_exc())

    def generate_metadata(self):
        try:
            old_standardised_df = read_csv_from_buffer_bucket(
                self.bucket, self.config["standardised_data_path"]
            )
            old_row_count = len(old_standardised_df.index)
        except Exception as e:
            old_row_count = 0

        new_row_count = len(self.standardised_df.index)
        timestamp_range = pd.to_datetime(
            self.standardised_df["bid_opening_date"].dropna(), errors="coerce"
        ).dt.date

        self.metadata.create_structure()

        self.metadata.create_metadata(
            df=self.standardised_df,
            source="eProcurements India High Value Central Tenders",
            source_abbr="EPIHVTC",
            sector=self.standardised_df["sector"].dropna().unique().tolist(),
            subsector=self.standardised_df["subsector"].dropna().unique().tolist(),
            source_tags=[],
            country_codes=self.standardised_df["country_code"].unique().tolist(),
            frequency="daily",
            dataset_type="T",
            indicatorfile="indicators_epihvtc.json",
            datasetfile=self.config["standardised_data_path"],
            timestamp_coverage=[str(timestamp_range.min()), str(timestamp_range.max())],
            no_of_proj_tenders=new_row_count,
            no_of_new_proj_tenders=(new_row_count - old_row_count),
        )
        print("Generated metadata")

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
            geocoded_data = self.load_data()
            self.standardised_df = self.standardise_data(geocoded_data)
            self.generate_metadata()
        except Exception as e:
            print(f"Unable to geocode data: {e}", traceback.print_exc())
        finally:
            self.bucket.upload_file(
                filename=os.path.join(self.metadata.base_folder, "metadata.json"),
                key=self.config["metadata_path"],
            )
            self.save_data(self.standardised_df, self.config["standardised_data_path"])


if __name__ == "__main__":
    path_config = load_config_yaml()["paths"]["EPIHVTC"]
    config = {
        "columns": [
            "tender_category",
            "product_category",
            "product_sub_category",
            "title",
        ],
        "geocoded_data_path": path_config["geocoded_data_path"],
        "standardised_data_path": path_config["standardized_data_path"],
    }
    standardizer = EPIStandardiser(config=config)
    standardizer.run()
