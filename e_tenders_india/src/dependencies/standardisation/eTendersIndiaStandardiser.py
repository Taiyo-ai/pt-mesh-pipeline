import os
import re
import traceback
import pandas as pd
import numpy as np

from .standardizer import sector_sub_sector_update
from ..utils import load_config_yaml
from ..utils.bucket import (
    connect_to_buffer_bucket,
    push_csv_to_buffer_bucket,
    read_csv_from_buffer_bucket,
)
from ..utils.metadata import Metadata


class eTendersIndiaStandardiser:
    def __init__(self, **kwargs):
        self.config: dict = kwargs.get("config")
        self.bucket = connect_to_buffer_bucket()
        self.standardised_df: pd.DataFrame = None
        self.metadata = Metadata(
            name="etendersindia", bucket="taiyo-projects", aws=False
        )

    def rename_columns(self, df: pd.DataFrame):
        renaming_dict = {
            "organisation_chain": "organisation_chain",
            "tender_reference_number": "tender_reference_number",
            "tender_id": "original_id",
            "tender_type": "tender_type",
            "tender_category": "sector",
            "general_technical_evaluation_allowed": "general_technical_evaluation_allowed",
            "payment_mode": "payment_mode",
            "is_multi_currency_allowed_for_fee": "is_multi_currency_allowed_for_fee",
            "form_of_contract": "form_of_contract",
            "no._of_covers": "no._of_covers",
            "itemwise_technical_evaluation_allowed": "itemwise_technical_evaluation_allowed",
            "is_multi_currency_allowed_for_boq": "is_multi_currency_allowed_for_boq",
            "allow_two_stage_bidding": "allow_two_stage_bidding",
            "instrument_type": "instrument_type",
            "cover_details": "cover_details",
            "tender_fee_in_₹": "tender_fee_in_₹",
            "tender_fee_in_usd": "tender_fee_in_usd",
            "fee_payable_to": "fee_payable_to",
            "tender_fee_exemption_allowed": "tender_fee_exemption_allowed",
            "fee_payable_at": "fee_payable_at",
            "emd_amount_in_₹": "emd_amount_in_₹",
            "emd_amount_in_usd": "emd_amount_in_usd",
            "emd_fee_type": "emd_fee_type",
            "emd_payable_to": "emd_payable_to",
            "emd_through_bg/st_or_emd_exemption_allowed": "emd_through_bg_st_or_emd_exemption_allowed",
            "emd_percentage": "emd_percentage",
            "emd_payable_at": "emd_payable_at",
            "title": "name",
            "work_description": "description",
            "nda/pre_qualification": "nda_pre_qualification",
            "independent_external_monitor/remarks": "independent_external_monitor_remarks",
            "tender_value_in_₹": "tender_value_in_₹",
            "tender_value_in_usd": "budget",
            "contract_type": "contract_type",
            "location": "location",
            "pre_bid_meeting_address": "pre_bid_meeting_address",
            "should_allow_nda_tender": "should_allow_nda_tender",
            "sub_category": "subsector",
            "period_of_work(days)": "period_of_work(days)",
            "pre_bid_meeting_place": "pre_bid_meeting_place",
            "bid_opening_place": "bid_opening_place",
            "product_category": "product_category",
            "bid_validity(days)": "bid_validity(days)",
            "pincode": "pincode",
            "pre_bid_meeting_date": "pre_bid_meeting_date",
            "allow_preferential_bidder": "allow_preferential_bidder",
            "published_date": "published_date",
            "document_download_/_sale_start_date": "document_download_sale_start_date",
            "clarification_start_date": "clarification_start_date",
            "bid_submission_start_date": "bid_submission_start_date",
            "bid_opening_date": "bid_opening_date",
            "document_download_/_sale_end_date": "document_download_sale_end_date",
            "clarification_end_date": "clarification_end_date",
            "bid_submission_end_date": "bid_submission_end_date",
            "url": "url",
            "bank_name": "bank_name",
            "name": "contact_name",
            "address": "contact_address",
            "data_source": "source",
            "country_code": "country_code",
            "country": "country",
            "map_coordinates": "map_coordinates",
            "aug_id": "aug_id",
            "project_or_tender": "project_or_tender",
            "label": "label",
            "state": "state",
            "county": "county",
            "locality": "locality",
            "neighbourhood": "neighbourhood",
        }
        return df.rename(columns=renaming_dict)

    def typecast_df(self, df: pd.DataFrame) -> pd.DataFrame:
        df.fillna(np.nan, inplace=True)
        df["map_coordinates"] = df["map_coordinates"].apply(lambda x: [eval(x)])

        df["budget"] = df["budget"].apply(lambda x: re.sub(r"[^0-9.]", "", str(x)))
        df["budget"] = df["budget"].apply(lambda x: ".".join(x.split(".")[:1]))

        for col in df.columns:
            df[col] = df[col].apply(lambda x: "nan" if x == "" else x)

        df["organisation_chain"].astype(str)
        df["tender_reference_number"].astype(str)
        df["original_id"].astype(str)
        df["tender_type"].astype(str)
        df["sector"].astype(str)
        df["general_technical_evaluation_allowed"].astype(str)
        df["payment_mode"].astype(str)
        df["is_multi_currency_allowed_for_fee"].astype(str)
        df["form_of_contract"].astype(str)
        df["no._of_covers"].astype("float64")
        df["itemwise_technical_evaluation_allowed"].astype(str)
        df["is_multi_currency_allowed_for_boq"].astype(str)
        df["allow_two_stage_bidding"].astype(str)
        df["instrument_type"].astype(str)
        df["cover_details"].astype(str)
        df["tender_fee_in_₹"].astype("float64")
        df["fee_payable_to"].astype(str)
        df["tender_fee_exemption_allowed"].astype(str)
        df["fee_payable_at"].astype(str)
        df["emd_amount_in_₹"].astype("float64")
        df["emd_fee_type"].astype(str)
        df["emd_payable_to"].astype(str)
        df["emd_through_bg_st_or_emd_exemption_allowed"].astype(str)
        df["emd_percentage"].astype(str)
        df["emd_payable_at"].astype(str)
        df["name"].astype(str)
        df["description"].astype(str)
        df["nda_pre_qualification"].astype(str)
        df["independent_external_monitor_remarks"].astype(str)
        df["tender_value_in_₹"].astype("float64")
        df["contract_type"].astype(str)
        df["location"].astype(str)
        df["pre_bid_meeting_address"].astype(str)
        df["should_allow_nda_tender"].astype(str)
        df["subsector"].astype(str)
        df["period_of_work(days)"].astype("float64")
        df["pre_bid_meeting_place"].astype(str)
        df["bid_opening_place"].astype(str)
        df["product_category"].astype(str)
        df["bid_validity(days)"].astype("float64")
        df["pincode"].astype("float64")
        df["pre_bid_meeting_date"].astype(str)
        df["allow_preferential_bidder"].astype(str)
        df["published_date"].astype(str)
        df["document_download_sale_start_date"].astype(str)
        df["clarification_start_date"].astype(str)
        df["bid_submission_start_date"].astype(str)
        df["bid_opening_date"].astype(str)
        df["document_download_sale_end_date"].astype(str)
        df["clarification_end_date"].astype(str)
        df["bid_submission_end_date"].astype(str)
        df["contact_name"].astype(str)
        df["contact_address"].astype(str)
        df["url"].astype(str)
        df["bank_name"].astype(str)
        df["source"].astype(str)
        df["country_code"].astype(str)
        df["country"].astype(str)
        df["map_coordinates"].astype(str)
        df["aug_id"].astype(str)
        df["project_or_tender"].astype(str)
        df["tender_fee_in_usd"].astype("float64")
        df["emd_amount_in_usd"].astype("float64")
        df["budget"].astype(str)
        df["label"].astype(str)
        df["state"].astype(str)
        df["county"].astype(str)
        df["locality"].astype(str)
        df["neighbourhood"].astype(str)
        df["identified_sector"].astype(str)
        df["identified_subsector"].astype(str)
        df["identified_sector_subsector_tuple"].astype(str)

        df["subsector"] = "Not Available"
        df["region_name"] = "South Asia"
        df["region_code"] = "SAS"

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
            df["identified_status"] = "Active"
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
            self.standardised_df.dropna(subset=["published_date"])[
                "published_date"
            ].astype("str")
        ).dt.date

        self.metadata.create_structure()

        self.metadata.create_metadata(
            df=self.standardised_df,
            source="eTenders India",
            source_abbr="ETENDERSINDIA",
            sector=self.standardised_df.dropna(subset=["sector"])["sector"]
            .unique()
            .tolist(),
            subsector=self.standardised_df.dropna(subset=["subsector"])["subsector"]
            .unique()
            .tolist(),
            source_tags=[],
            country_codes=self.standardised_df.dropna(subset=["country_code"])[
                "country_code"
            ]
            .unique()
            .tolist(),
            frequency="daily",
            dataset_type="P",
            indicatorfile="indicators_etendersindia.json",
            datasetfile=self.config["standardised_data_path"],
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
            geocoded_data = self.load_data()
            self.standardised_df = self.standardise_data(geocoded_data)
            self.generate_metadata()
        except Exception as e:
            print(f"Unable to standardise data: {e}", traceback.print_exc())
        finally:
            print("Uploading...")
            self.bucket.upload_file(
                filename=os.path.join(self.metadata.base_folder, "metadata.json"),
                key=self.config["metadata_path"],
            )
            # self.standardised_df.to_csv(
            #     "etendersindia_standardised.csv", index=False, header=True
            # )
            self.save_data(self.standardised_df, self.config["standardised_data_path"])


if __name__ == "__main__":
    path_config = load_config_yaml()["paths"]["ETENDERSINDIA"]
    path_config["columns"] = ["tender_category", "sub_category", "product_category"]
    standardizer = eTendersIndiaStandardiser(config=path_config)
    standardizer.run()
