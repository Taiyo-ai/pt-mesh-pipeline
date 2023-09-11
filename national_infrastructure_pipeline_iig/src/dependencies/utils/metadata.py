import json
import os
import sys
import pandas as pd

from typing import Any
from pathlib import PurePosixPath

from .s3_bucket import S3Bucket


class Metadata:
    def __init__(self, name: str, bucket: str, aws: bool) -> None:
        """Creates the data and metadata files/folder structure"""

        self.name = name
        self.aws = aws or False

        # AWS Lambda only provides access to /tmp
        self.base_folder = os.path.join(
            os.path.abspath(".").split(os.path.sep)[0] + os.path.sep,
            "tmp",
            self.name,
            "metadata",
        )

        # For upload on AWS S3
        self.s3_folder = PurePosixPath(self.name, "metadata")

        if self.aws:
            self.bucket = S3Bucket(bucket)

        self.indicators = {}

    def create_structure(self):
        """Creates the barebone folder structure and empty metadata.json files"""

        foldername = self.base_folder
        os.makedirs(foldername, exist_ok=True)

        filename = os.path.join(foldername, "metadata.json")

        with open(filename, "w") as f:
            json.dump([], f)

        # AWS
        if self.aws:
            print("\n")
            self.bucket.upload_file(
                filename=filename,
                key=str(PurePosixPath(self.s3_folder, "metadata.json")),
            )

    def create_indicators(self, df: Any, indicatorfile: str):
        """Creates indicator array for dataframe by reading from a file line by line"""
        with open(os.path.join(sys.path[0], "dependencies", indicatorfile), "r") as f:
            indicators = json.load(f)
            for index, column in enumerate(df.columns):
                code = column.lower()
                if "timestamp" not in code:
                    try:
                        self.indicators[code] = indicators[code]
                    except KeyError:
                        self.indicators[code] = {"description": "NA", "unit": "NA"}

    def add_metadata(
        self,
        df: Any,
        source: str,
        source_abbr: str,
        sector: list,
        subsector: list,
        source_tags: list,
        country_codes: list,
        frequency: str,
        dataset_type: str,
        indicatorfile: str,
        datasetfile: str,
        timestamp_coverage: list,
        no_of_proj_tenders: int,
        no_of_new_proj_tenders: int,
    ):
        """
        Adds a metadata object for a source in metadata.json

        You maybe looking for create_metadata(), **Use this only in case of multiple dataset files**

        params:
            df:                     Cleaned DataFrame
            source:                 Source Name
            source_abbr:            Source Name Abbreviation
            sector:                 Aggregated sector tags
            subsector:              Aggregated sub sector tags
            source_tags:            Aggregated source tags
            country_codes:          List of country codes in ISO-3 format
            frequency:              Frequency of update
            dataset_type:           Type of Data (P for Projects, T for Tenders)
            indicatorfile:          name of indicator file
            datasetfile:            Path to Dataset file
            timestamp_coverage:     Timespan coverage of data
            no_of_proj_tenders:     Total number of projects/tenders
            no_of_new_proj_tenders: Number of new projects/tenders added
        returns:
            None
        """

        filename = os.path.join(self.base_folder, "metadata.json")
        indicators_present = False

        # verify indicators are present
        if len(self.indicators) != len(df.columns):
            try:
                self.create_indicators(df, indicatorfile)
                indicators_present = True
            except Exception as e:
                print(e)
        else:
            indicators_present = True

        # Add preliminary data
        with open(filename, "r+") as f:
            metadata = json.load(f)
            metadata.append(
                {
                    "source": source,
                    "source_abbr": source_abbr,
                    "sector": sector,
                    "subsector": subsector,
                    "source_tags": source_tags,
                    "country_codes": country_codes,
                    "dataset_type": dataset_type,
                    "frequency": frequency,
                    "filename": datasetfile,
                    "timestamp_coverage": timestamp_coverage,
                    "no_of_proj_tenders": no_of_proj_tenders,
                    "no_of_new_proj_tenders": no_of_new_proj_tenders,
                    "ingested_timestamp": str(pd.Timestamp.utcnow()),
                    "last_update_timestamp": str(pd.Timestamp.utcnow()),
                    "columns": {},
                }
            )
            f.seek(0)
            json.dump(metadata, f, indent=4)
            f.truncate()

        for index, column in enumerate(df.columns):
            code = column.lower()
            if "timestamp" not in code:
                indicator = (
                    self.indicators[code]
                    if indicators_present
                    else {"description": "NA", "unit": "NA"}
                )
                if not df.empty:
                    latest = str(df[column].iloc[-1])
                    data_type = str(df.dtypes[column])
                else:
                    latest = "NA"
                    data_type = "NA"

                with open(filename, "r+") as f:
                    metadata = json.load(f)
                    for index, data in enumerate(metadata):
                        if data["filename"] == datasetfile:
                            metadata[index]["columns"].update(
                                {
                                    code: {
                                        "name": code,
                                        "description": indicator["description"],
                                        "type": data_type,
                                        "unit": indicator["unit"],
                                        "timestamp": str(pd.Timestamp.utcnow()),
                                        "value": latest,
                                    }
                                }
                            )
                    f.seek(0)
                    json.dump(metadata, f, indent=4)
                    f.truncate()

        # AWS
        if self.aws:
            print("\n")
            self.bucket.upload_file(
                filename=filename,
                key=str(PurePosixPath(self.s3_folder, "metadata.json")),
            )

    def update_metadata(self, df: Any, datasetfile: str, filename: str):
        for column in df.columns:
            code = column.lower()
            if "timestamp" not in code:
                if not df.empty:
                    latest = str(df[column].iloc[-1])
                else:
                    latest = 0

                with open(filename, "r+") as f:
                    metadata = json.load(f)
                    for index, data in enumerate(metadata):
                        if data["filename"] == datasetfile:
                            metadata[index]["ingested_timestamp"] = str(
                                pd.Timestamp.utcnow()
                            )
                            metadata[index]["columns"][code].update(
                                {
                                    "timestamp": str(pd.Timestamp.utcnow()),
                                    "value": latest,
                                }
                            )
                    f.seek(0)
                    json.dump(metadata, f, indent=4)
                    f.truncate()

    def create_metadata(
        self,
        df: Any,
        source: str,
        source_abbr: str,
        sector: list,
        subsector: list,
        source_tags: list,
        country_codes: list,
        frequency: str,
        dataset_type: str,
        indicatorfile: str,
        datasetfile: str,
        timestamp_coverage: list,
        no_of_proj_tenders: int,
        no_of_new_proj_tenders: int,
    ):
        """
        Populates the metadata.json file, should be called after create_structure()

        params:
            df:                     Cleaned DataFrame
            source:                 Source Name
            source_abbr:            Source Name Abbreviation
            sector:                 Aggregated sector tags
            subsector:              Aggregated sub sector tags
            source_tags:            Aggregated source tags
            country_codes:          List of country codes in ISO-3 format
            frequency:              Frequency of update
            dataset_type:           Type of Data (P for Projects, T for Tenders)
            indicatorfile:          name of indicator file
            datasetfile:            Path to Dataset file
            timestamp_coverage:     Timespan coverage of data
            no_of_proj_tenders:     Total number of projects/tenders
            no_of_new_proj_tenders: Number of new projects/tenders added
        returns:
            None
        """
        self.create_indicators(df, indicatorfile)

        self.add_metadata(
            df,
            source,
            source_abbr,
            sector,
            subsector,
            source_tags,
            country_codes,
            frequency,
            dataset_type,
            indicatorfile,
            datasetfile,
            timestamp_coverage,
            no_of_proj_tenders,
            no_of_new_proj_tenders,
        )


if __name__ == "__main__":
    # Use the harvested dataframe here
    df = pd.DataFrame.from_dict({"pizza": [1], "burger": [2], "fries": [3]})

    # Don't change the env and bucket name in development
    country_metadata = Metadata(name="dummy", bucket="test-bucket-taiyo", aws=False)

    # Create structure (files and folders)
    country_metadata.create_structure()

    # Populate the folders
    country_metadata.create_metadata(
        df=df,
        source="National Infrastructure Pipline - IIG",
        source_abbr="IIG",
        sector=["some sector"],
        subsector=["subsector here"],
        source_tags=["source tags"],
        country_codes=["IND"],  # ISO-3
        frequency="bi-monthly",
        dataset_type="P",
        indicatorfile="indicators_iig.json",
        datasetfile="iig_cleaned.csv",
        timestamp_coverage=["2004-5-4", "2021-07-14"],
        no_of_proj_tenders=31546,
        no_of_new_proj_tenders=50,
    )
