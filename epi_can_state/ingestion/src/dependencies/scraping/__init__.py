import pandas as pd
import requests

from selenium import webdriver

from ..utils.bucket import (
    connect_to_buffer_bucket,
    push_csv_to_buffer_bucket,
    read_csv_from_buffer_bucket,
)


class BaseScraper:
    def __init__(self, driver_options=None, driver_executable_path=None):
        self.driver = None
        self.data_columns = ["project_id", "url"]
        self.master_df = None
        self.project_ids_urls_df = pd.DataFrame(columns=self.data_columns)
        self.success_urls = pd.DataFrame(columns=self.data_columns)
        self.failed_urls = pd.DataFrame(columns=self.data_columns)
        self.scraping_list_df = None
        self.collected_data = []

        # Connect to GCP Bucket
        self.bucket = connect_to_buffer_bucket()

        # Selenium webdriver configuration
        if driver_options is not None and driver_executable_path is not None:
            self.initialize_driver(driver_options, driver_executable_path)

    @staticmethod
    def get_html_for_url(url: str):
        r = requests.get(url)
        return r.text

    @staticmethod
    def get_driver_opts(list_of_opts):
        options = webdriver.ChromeOptions()
        for option in list_of_opts:
            options.add_argument(option)
        return options

    def initialize_driver(self, list_of_options, executable_path):
        options = BaseScraper.get_driver_opts(list_of_options)
        self.driver = webdriver.Chrome(executable_path=executable_path, options=options)

    def add_to_collected_data(self, page_data):
        self.collected_data.append(page_data)

    def add_url_to_success_list(self, project_id, url):
        self.success_urls = self.success_urls.append(
            {"project_id": project_id, "url": url}, ignore_index=True
        )

    def add_url_to_failed_list(self, project_id, url):
        self.failed_urls = self.failed_urls.append(
            {"project_id": project_id, "url": url}, ignore_index=True
        )

    def remove_from_project_ids_urls(self, project_id):
        self.project_ids_urls_df.drop(project_id, axis=0, inplace=True)

    def get_scraping_list_df(self):
        scraping_list = list(
            set([tuple(row) for row in self.project_ids_urls_df.values.tolist()])
            .difference(set([tuple(row) for row in self.failed_urls.values.tolist()]))
            .difference(set([tuple(row) for row in self.success_urls.values.tolist()]))
        )
        return pd.DataFrame(scraping_list, columns=self.data_columns)

    def load_data(
        self,
        reference_urls_path="",
        master_data_path="",
        success_urls_path="",
        failed_urls_path="",
    ):
        try:
            # self.master_df = pd.read_csv(master_data_path)
            self.master_df = read_csv_from_buffer_bucket(self.bucket, master_data_path)
        except Exception as e:
            print(f"Error occurred while loading data\n{str(e)}")

        try:
            # self.project_ids_urls_df = pd.read_csv(reference_urls_path)
            self.project_ids_urls_df = read_csv_from_buffer_bucket(
                self.bucket, reference_urls_path
            )
            print(f"Total urls: {self.project_ids_urls_df.shape[0]}")
        except Exception as e:
            print("Reference URLs file not found or please enter the correct path")

        try:
            # self.success_urls = pd.read_csv(success_urls_path)
            self.success_urls = read_csv_from_buffer_bucket(
                self.bucket, success_urls_path
            )
            print(f"Total successful urls: {len(self.success_urls)}")
        except Exception as e:
            self.success_urls = pd.DataFrame(columns=self.data_columns)
            print("Success urls file not found")

        try:
            # self.failed_urls = pd.read_csv(failed_urls_path)
            self.failed_urls = read_csv_from_buffer_bucket(
                self.bucket, failed_urls_path
            )
            print(f"Total failed urls: {len(self.failed_urls)}")
        except Exception as e:
            self.failed_urls = pd.DataFrame(columns=self.data_columns)
            print("Failed urls file not found")

        self.scraping_list_df = self.get_scraping_list_df()
        print(f"Total urls to be tried: {self.scraping_list_df.shape[0]}")

    def save_data(
        self, master_data_path, success_urls_path, failed_urls_path, drop_dups_cols=None
    ):
        if drop_dups_cols is None:
            drop_dups_cols = ["project_id"]
        if self.master_df is None:
            self.master_df = pd.DataFrame(self.collected_data)
        else:
            self.master_df = self.master_df.append(
                self.collected_data, ignore_index=True
            )
        self.master_df.drop_duplicates(drop_dups_cols, keep="last", inplace=True)
        # self.master_df.to_csv(master_data_path, index=False, header=True)
        push_csv_to_buffer_bucket(self.bucket, self.master_df, master_data_path)

        if success_urls_path:
            # self.success_urls.to_csv(success_urls_path, header=True, index=False)
            push_csv_to_buffer_bucket(self.bucket, self.success_urls, success_urls_path)
        if failed_urls_path:
            self.failed_urls = self.failed_urls[
                ~self.failed_urls["project_id"].isin(
                    self.success_urls.project_id.tolist()
                )
            ]
            # self.failed_urls.to_csv(failed_urls_path, header=True, index=False)
            push_csv_to_buffer_bucket(self.bucket, self.failed_urls, failed_urls_path)
