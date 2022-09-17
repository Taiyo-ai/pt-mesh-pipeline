import os
import pandas as pd
import yaml
import numpy as np
import traceback
import math


from opensearchpy import OpenSearch, RequestsHttpConnection, helpers
from requests_aws4auth import AWS4Auth
import boto3

from time import sleep

from ..utils import load_config_yaml
from ..utils.bucket import (
    connect_to_buffer_bucket,
    read_csv_from_buffer_bucket,
)



def coordinates_to_geopoint(coordinates):
    try:
        if coordinates == np.nan or math.isnan(coordinates):
            return None
    except:
        print("nan check failed")
    try: 
        coordinates = [eval(x) for x in coordinates]
    except:
        print("list(str) to coords failed")
    doc = {}
    doc["lat"] = coordinates[0] if coordinates[0] >= -90 and coordinates[0] <= 90 else 'null'
    doc["lon"] = coordinates[1] if coordinates[1] >= -180 and coordinates[1] <= 180 else 'null'
    if doc["lat"] == 'null' or doc["lon"] == 'null':
        return None
    return doc


class eTendersIndiaIngestion:
    def __init__(self, config) -> None:
        self.config = config
        self.pri_index = "tendersv2_pri_etenders"
        self.sec_index = "tendersv2_sec_etenders"
        host = os.getenv("ELASTICSEARCH_URL") # For example, my-test-domain.us-east-1.es.amazonaws.com        
        region = 'eu-west-3'
        service = 'es'

        credentials = boto3.Session(aws_access_key_id=os.getenv("ELASTICSEARCH_USER"), aws_secret_access_key=os.getenv("ELASTICSEARCH_PASS")).get_credentials()
        awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
        self.client = OpenSearch(
            hosts = [{'host': host, 'port': 443}],
            http_auth = awsauth,
            use_ssl = True,
            verify_certs = True,
            connection_class = RequestsHttpConnection,
            request_timeout=3600,
            timeout=3600,
        )

    def extract_fields(self):
        with open('mappings_pri.yaml') as f:
            pri_fields = yaml.load(f)
            pri_fields = list(pri_fields["mappings"]["properties"].keys())
        
        with open('mappings_sec.yaml') as f:
            sec_fields = yaml.load(f)
            sec_fields = list(sec_fields["mappings"]["properties"].keys())

        return pri_fields, sec_fields

    def run(self):
        path = self.config["standardised_data_path"]
        pri_doc_list, sec_doc_list = self.load_data(path)
        

        # use the helpers library's Bulk API to index list of Elasticsearch docs
        try:
            print(f"\nBulk inserting the doc_list to {self.pri_index}, {self.sec_index} index")
            self.client.indices.delete(index=self.pri_index, ignore=[400, 404])
            self.client.indices.delete(index=self.sec_index, ignore=[400, 404])

            with open('./mappings_pri.yaml', 'r') as f:
                pri_mappings = yaml.load(f)
            with open('./mappings_sec.yaml', 'r') as f:
                sec_mappings = yaml.load(f)
           
            print(f"creating {self.pri_index}, {self.sec_index} index...")

            self.client.indices.create(index = self.pri_index, body = pri_mappings)
            self.client.indices.create(index = self.sec_index, body = sec_mappings)
            
            resp = helpers.bulk(
                self.client, pri_doc_list, index=self.pri_index, doc_type="_doc"
            )
            resp = helpers.bulk(
                self.client, sec_doc_list, index=self.sec_index, doc_type="_doc"
            )

            print("\nindices generated for set")
            print("\nrefreshing indices")
            sleep(30)
            self.client.indices.refresh(index=self.pri_index)
            self.client.indices.refresh(index=self.sec_index)
            print("\nindices refreshed")
        except Exception as e:
            print("\nEncountered Problem: ", e)
            print(traceback.print_exc())

    def load_data(self, path):
        try:
            pri_doc_list, sec_doc_list = [], []
            print("\nGenerating doc_list")
            bucket = connect_to_buffer_bucket()
            df = read_csv_from_buffer_bucket(bucket, path)
            df = df.where(pd.notnull(df), None)
            df["country_name"] = "India"
            df.identified_sector_subsector_tuple = (
                df.identified_sector_subsector_tuple.map(lambda x: eval(x))
            )
            df["map_coordinates"] = df["map_coordinates"].apply(
                lambda x: eval(x) if x is not None else x
            )
            df = df.explode('map_coordinates')
            df["map_coordinates"] = df["map_coordinates"].apply(
                lambda x: coordinates_to_geopoint(x) if x is not None else x
            )

            pri_fields, sec_fields = self.extract_fields()

            pri_doc_list = df[df.columns.intersection(pri_fields)].to_dict(orient="records")
            sec_doc_list = df[df.columns.intersection(sec_fields)].to_dict(orient="records")
            print("\nSuccesfully generated doc_list")
        except Exception as e:
            print("Encountered Problem while generating doc_list", e)
            print(traceback.print_exc())

        return pri_doc_list, sec_doc_list


if __name__ == "__main__":
    config = load_config_yaml()["paths"]["ETENDERSINDIA"]
    eTendersIndiaIngestion(config=config).run()
