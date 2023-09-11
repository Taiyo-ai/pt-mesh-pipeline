import os
import pandas as pd

from elasticsearch import Elasticsearch, helpers

from time import sleep

from ..utils import load_config_yaml
from ..utils.bucket import (
    connect_to_buffer_bucket,
    read_csv_from_buffer_bucket,
)


class IIGCSRIngestion:
    def __init__(self, config) -> None:
        self.config = config
        self.index = "projects_iigcsr"
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

    def run(self):
        path = self.config["standardized_data_path"]
        doc_list = self.load_data(path)

        # use the helpers library's Bulk API to index list of Elasticsearch docs
        try:
            self.client.indices.delete(index=self.index, ignore=[400, 404])
        except Exception as e:
            print("Failed to delete index")

        try:
            print(f"\nBulk inserting the doc_list to {self.index} index")
            resp = helpers.bulk(
                self.client, doc_list, index=self.index, doc_type="_doc"
            )
            print("\nindices generated for set")
            print("\nrefreshing indices")
            self.client.indices.refresh(index=self.index)
            print("\nindices refreshed")
        except Exception as e:
            print("\nEncountered Problem: ", e)
            with open("error.txt", "w") as f:
                f.write(str(e))

    def load_data(self, path):
        try:
            doc_list = []
            print("\nGenerating doc_list")
            bucket = connect_to_buffer_bucket()
            df = read_csv_from_buffer_bucket(bucket, path)
            df = df.where(pd.notnull(df), None)
            df["map_coordinates"] = df["map_coordinates"].apply(lambda x: eval(x))
            df["identified_sector_subsector_tuple"] = df[
                "identified_sector_subsector_tuple"
            ].apply(lambda x: eval(x))
            doc_list = df.to_dict(orient="records")
            print("\nSuccesfully generated doc_list")
        except Exception as e:
            print("Encountered Problem while generating doc_list", e)

        return doc_list


if __name__ == "__main__":
    config = load_config_yaml()["paths"]["IIG_CSR"]
    IIGCSRIngestion(config=config).run()
