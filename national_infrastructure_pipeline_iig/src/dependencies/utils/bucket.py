import traceback
import json
import pandas as pd

from io import BytesIO
from pandas import DataFrame
from .s3_bucket import S3Bucket


def connect_to_buffer_bucket(BUCKET_NAME="taiyo-projects"):
    bucket = None
    try:
        bucket = S3Bucket(bucket=BUCKET_NAME)
        print(f'Successfully connected to the bucket "{BUCKET_NAME}"')
        return bucket
    except Exception as e:
        print(
            f'{e}\nError connecting to bucket "{BUCKET_NAME}": Please check the credentials again.'
        )


def push_csv_to_buffer_bucket(bucket: S3Bucket, dataframe: DataFrame, rel_path: str):
    try:
        buffer = BytesIO(
            bytes(
                dataframe.to_csv(index=False, header=True, compression="gzip"),
                encoding="utf-8",
            )
        )

        bucket.upload_file(fileobj=buffer, key=rel_path)
        print(f'Successfully pushed the csv file to "{rel_path}"')
    except Exception as e:
        print(f'{e}\nError occured while pushing file to bucket path "{rel_path}"')


def read_csv_from_buffer_bucket(bucket: S3Bucket, rel_path: str):
    try:
        buffer = BytesIO()
        key = list(bucket.search(rel_path))

        if not key:
            raise FileNotFoundError

        key = str(key[0].key)
        bucket.download_file(key=key, fileobj=buffer)
        buffer.seek(0)

        extension = rel_path.split(".")[-1]
        if extension == "csv":
            dataframe = pd.read_csv(buffer, sep=",")
            return dataframe
    except Exception as e:
        print(f"{e}\nFailed to read csv from bucket. {rel_path}")


def push_json_to_buffer_bucket(bucket: S3Bucket, json_obj: dict, rel_path: str):
    try:
        buffer = BytesIO(bytes(json.dumps(json_obj).encode("utf-8")))
        bucket.upload_file(fileobj=buffer, key=rel_path)
        print(f'Successfully pushed the json file to "{rel_path}"')
    except Exception as e:
        print(f'{e}\nError occured while pushing file to bucket path "{rel_path}"')


def read_json_from_buffer_bucket(bucket: S3Bucket, rel_path: str):
    try:
        buffer = BytesIO()
        key = list(bucket.search(rel_path))

        if not key:
            raise FileNotFoundError

        key = str(key[0].key)
        bucket.download_file(key=key, fileobj=buffer)
        buffer.seek(0)

        extension = rel_path.split(".")[-1]
        if extension == "json":
            json_data = json.load(buffer)
            return json_data
    except Exception as e:
        print(f"{e}\nFailed to read json from bucket.")


def read_excel_from_buffer_bucket(bucket: S3Bucket, sheet_name: str, rel_path: str):
    try:
        buffer = BytesIO()
        key = list(bucket.search(rel_path))

        if not key:
            raise FileNotFoundError

        key = str(key[0].key)
        bucket.download_file(key=key, fileobj=buffer)
        buffer.seek(0)

        extension = rel_path.split(".")[-1]
        if extension == "xlsx":
            if sheet_name:
                dataframe = pd.read_excel(buffer, sheet_name=sheet_name)
            else:
                dataframe = pd.read_excel(buffer)
            return dataframe
    except Exception as e:
        print(f"{e}\nFailed to read excel from bucket.")


def read_stata_from_buffer_bucket(bucket: S3Bucket, rel_path: str, iterator=False):
    try:
        buffer = BytesIO()
        key = list(bucket.search(rel_path))

        if not key:
            raise FileNotFoundError

        key = str(key[0].key)
        bucket.download_file(key=key, fileobj=buffer)
        buffer.seek(0)

        extension = rel_path.split(".")[-1]
        if extension == "dta":
            dataframe = pd.read_stata(buffer, iterator=iterator)
            return dataframe
    except Exception as e:
        print(f"{e}\nFailed to read stata from bucket.")
