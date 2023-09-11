import os
import sys
import math
import yaml
import traceback
import pandas as pd
import numpy as np

from elasticsearch import Elasticsearch, helpers

from time import sleep

from ..utils import load_config_yaml
from ..utils.bucket import (
    connect_to_buffer_bucket,
    read_csv_from_buffer_bucket,
)


class EPIIngestion:
    def __init__(self, config) -> None:
        self.config = config
        self.bucket = connect_to_buffer_bucket()

        self.pri_index = "tendersv2_pri_epihvtstate"
        self.sec_index = "tendersv2_sec_epihvtstate"

        self.primary_mappings_path = os.path.join(
            sys.path[0], "dependencies", "utils", "mappings", "mappings_pri.yaml"
        )
        self.secondary_mappings_path = os.path.join(
            sys.path[0], "dependencies", "utils", "mappings", "mappings_sec.yaml"
        )

        self.client = Elasticsearch(
            [os.getenv("ELASTICSEARCH_URL")],
            http_auth=(
                os.getenv("ELASTICSEARCH_USER"),
                os.getenv("ELASTICSEARCH_PASS"),
            ),
            scheme="https",
            port=443,
            use_ssl=True,
            request_timeout=3600,
            timeout=3600,
        )

    def coordinates_to_geopoint(self, coordinates):
        try:
            if coordinates == np.nan or math.isnan(coordinates):
                return None
        except Exception as e:
            print("nan check failed")
        doc = {}
        doc["lat"] = (
            coordinates[0] if coordinates[0] >= -90 and coordinates[0] <= 90 else "null"
        )
        doc["lon"] = (
            coordinates[1]
            if coordinates[1] >= -180 and coordinates[1] <= 180
            else "null"
        )
        if doc["lat"] == "null" or doc["lon"] == "null":
            return None
        return doc

    def extract_fields(self):
        with open(self.primary_mappings_path) as f:
            pri_fields = yaml.load(f)
            pri_fields = list(pri_fields["mappings"]["properties"].keys())

        with open(self.secondary_mappings_path) as f:
            sec_fields = yaml.load(f)
            sec_fields = list(sec_fields["mappings"]["properties"].keys())

        return pri_fields, sec_fields

    def load_data(self, path):
        pri_doc_list, sec_doc_list = [], []
        try:
            print("\nGenerating doc_list")

            df = read_csv_from_buffer_bucket(self.bucket, path)
            df = df.where(pd.notnull(df), None)

            df["timestamps"] = df["timestamps"].apply(eval)
            df["timestamp_range"] = df["timestamp_range"].apply(eval)

            df["map_coordinates"] = df["map_coordinates"].apply(lambda x: eval(x))
            df = df.explode("map_coordinates")
            df["map_coordinates"] = df["map_coordinates"].apply(
                lambda x: self.coordinates_to_geopoint(x) if x is not None else x
            )

            df["identified_sector_subsector_tuple"] = df[
                "identified_sector_subsector_tuple"
            ].apply(lambda x: eval(x))

            pri_fields, sec_fields = self.extract_fields()
            pri_doc_list = df.loc[:, pri_fields].to_dict(orient="records")
            sec_doc_list = df.loc[:, sec_fields].to_dict(orient="records")

            print("\nSuccesfully generated doc_list")
        except Exception as e:
            print("Encountered Problem while generating doc_list", e)
            print(traceback.format_exc())

        return pri_doc_list, sec_doc_list

    def run(self):
        path = self.config["standardized_data_path"]
        pri_doc_list, sec_doc_list = self.load_data(path)

        # use the helpers library's Bulk API to index list of Elasticsearch docs
        print(
            f"\nBulk inserting the doc_list to {self.pri_index}, {self.sec_index} index"
        )
        try:
            self.client.indices.delete(index=self.pri_index, ignore=[400, 404])
            self.client.indices.delete(index=self.sec_index, ignore=[400, 404])
        except Exception as e:
            print("Failed to delete index")

        try:
            with open(self.primary_mappings_path, "r") as f:
                pri_mappings = yaml.load(f)
            with open(self.secondary_mappings_path, "r") as f:
                sec_mappings = yaml.load(f)

            print(f"Creating {self.pri_index}, {self.sec_index} index...")

            self.client.indices.create(index=self.pri_index, body=pri_mappings)
            self.client.indices.create(index=self.sec_index, body=sec_mappings)

            resp = helpers.bulk(
                self.client, pri_doc_list, index=self.pri_index, doc_type="_doc"
            )
            resp = helpers.bulk(
                self.client, sec_doc_list, index=self.sec_index, doc_type="_doc"
            )

            print("\nIndices generated for set")
            print("\nRefreshing indices")
            sleep(30)
            self.client.indices.refresh(index=self.pri_index)
            self.client.indices.refresh(index=self.sec_index)
            print("\nIndices refreshed")

        except Exception as e:
            print("\nEncountered Problem: ", e)
            with open("error.txt", "w") as f:
                f.write(str(e))


if __name__ == "__main__":
    config = load_config_yaml()["paths"]["EPIHVTS"]
    EPIIngestion(config=config).run()
