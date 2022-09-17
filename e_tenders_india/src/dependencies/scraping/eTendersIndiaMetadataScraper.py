import os
import ssl
import sys
import requests
import traceback
import multiprocessing

import pandas as pd

from tqdm import tqdm
from bs4 import BeautifulSoup

from .eTendersIndia import ETendersIndiaScraper
from ..utils import load_config_yaml
from ..utils.bucket import (
    push_csv_to_buffer_bucket,
    read_csv_from_buffer_bucket,
)


if not os.environ.get("PYTHONHTTPSVERIFY", "") and getattr(
    ssl, "_create_unverified_context", None
):
    ssl._create_default_https_context = ssl._create_unverified_context


class eTendersIndiaMetadataScraper:
    def __init__(self, **kwargs):
        self.collected_data = []
        self.meta_data = None
        self.allurl = []

        self.second_collected_data = []
        self.second_meta_data = []
        self.tmp_collected_data = []
        self.metaurl = []
        self.config = kwargs.get("config")

        self.main_scraper = ETendersIndiaScraper(self.config)
        self.bucket = self.main_scraper.bucket

    def extract_data(self, html_page, url_name):
        self.allurl = []
        try:
            soup = BeautifulSoup(html_page.text, "lxml")

            for a in soup.find_all("a", href=True):
                page_data = {"url": ""}
                value = f"{url_name}{a['href']}"
                if "/app;jsessionid=" in value:
                    data = value
                    if "DirectLink&page=" in data:
                        self.allurl.append(data)

                self.collected_data.append(page_data)
        except Exception as e:
            print("Error occurred :", e)

    def extract_metasecond(self, html_page, url_name):
        try:
            soup2 = BeautifulSoup(html_page.text, "lxml")
            for a in soup2.find_all("a", href=True):
                second_page_data = {"metaurl": ""}
                value = f"{url_name}{a['href']}"
                if "/app;jsessionid=" in value:
                    data = value
                    if "DirectLink&page=" in data:
                        second_page_data["metaurl"] = data
                        # second_page_data["metaurl"] = re.sub(
                        #     r";jsessionid=.*\?",
                        #     "?",
                        #     str(data).replace("&session=T", ""),
                        # )

                self.second_collected_data.append(second_page_data)
                self.tmp_collected_data.append(second_page_data)
        except Exception as e:
            print("Error occurred :", e)

    def run2(self, url_name):
        self.tmp_collected_data = []
        try:
            print("Extracting Metadata...")
            for url in tqdm(self.allurl):
                html_page = requests.get(url)
                self.extract_metasecond(html_page, url_name)
        except Exception as e:
            print(
                f"Error occurred. Closing scraping process.\n{str(e)}",
                traceback.print_exc(),
            )

    def run3(self):
        try:
            self.main_scraper.master_df = read_csv_from_buffer_bucket(
                self.bucket, self.config["master_data_path"]
            )
        except Exception as e:
            print("Master Data not found, creating...")

        try:
            print("Extracting Data...")
            nan_value = float("NaN")

            tmp_df = pd.DataFrame(self.tmp_collected_data)
            # tmp_df.to_csv("tmp_df.csv", index=False, header=True)
            tmp_df.replace("", nan_value, inplace=True)
            tmp_df.dropna(subset=["metaurl"], inplace=True)
            tmp_df["tender_id"] = "dummy"

            pool = multiprocessing.Pool(processes=multiprocessing.cpu_count() - 1)
            final_result = pool.map(
                self.main_scraper.extract_data,
                tmp_df.values.tolist(),
            )

            pool.close()  # no more tasks
            pool.join()  # wrap up current tasks

            for result in final_result:
                if result["success"]:
                    self.main_scraper.add_to_collected_data(result["page_data"][0])
                    try:
                        self.main_scraper.add_url_to_success_list(
                            result["page_data"][0]["tender_id"],
                            result["page_data"][0]["url"],
                        )
                    except Exception as e:
                        self.main_scraper.add_url_to_success_list(
                            "NA",
                            result["page_data"][0]["url"],
                        )
                else:
                    self.main_scraper.add_url_to_failed_list(
                        "NA",
                        result["page_data"][0]["url"],
                    )
        except Exception as e:
            print(f"Error occurred. Closing scraping process.\n{traceback.print_exc()}")

    def save_data(self):
        try:
            self.second_meta_data = pd.DataFrame(self.second_collected_data)

            nan_value = float("NaN")
            self.second_meta_data.replace("", nan_value, inplace=True)
            self.second_meta_data.dropna(subset=["metaurl"], inplace=True)
            self.second_meta_data.rename(columns={"metaurl": "url"}, inplace=True)

            # self.second_meta_data.to_csv("finalurls.csv", index=False)
            push_csv_to_buffer_bucket(
                self.bucket, self.second_meta_data, self.config["base_data_path"]
            )

            self.second_meta_data["tender_id"] = "extracted_in_raw_data"
            push_csv_to_buffer_bucket(
                self.bucket, self.second_meta_data, self.config["reference_urls_path"]
            )

            # pd.DataFrame(self.main_scraper.collected_data).to_csv(
            #     "etendersindia_data.csv", index=False, header=True
            # )
            self.main_scraper.save_data(
                master_data_path=self.config["master_data_path"],
                success_urls_path=self.config["successful_urls_path"],
                failed_urls_path=self.config["failed_urls_path"],
                drop_dups_cols="tender_id",
            )
        except Exception as e:
            print(f"Error occurred while saving data.\n{str(e)}", traceback.print_exc())

    def run(self):
        states = [
            "https://etenders.gov.in/eprocure",
            "https://arunachaltenders.gov.in/nicgep",
            "https://assamtenders.gov.in/nicgep",
            "https://etenders.hry.nic.in/nicgep",
            "https://hptenders.gov.in/nicgep",
            "https://jharkhandtenders.gov.in/nicgep",
            "https://etenders.kerala.gov.in/nicgep",
            "https://mptenders.gov.in/nicgep",
            "https://mahatenders.gov.in/nicgep",
            "https://manipurtenders.gov.in/nicgep",
            "https://meghalayatenders.gov.in/nicgep",
            "https://mizoramtenders.gov.in/nicgep",
            "https://nagalandtenders.gov.in/nicgep",
            "https://www.tendersodisha.gov.in/nicgep",
            "https://eproc.punjab.gov.in/nicgep",
            "https://eproc.rajasthan.gov.in/nicgep",
            "https://sikkimtender.gov.in/nicgep",
            "https://tntenders.gov.in/nicgep",
            "https://tripuratenders.gov.in/nicgep",
            "https://etender.up.nic.in/nicgep",
            "https://uktenders.gov.in/nicgep",
            "https://wbtenders.gov.in/nicgep",
            "https://eprocure.andaman.gov.in/nicgep",
            "https://etenders.chd.nic.in/nicgep",
            "https://dnhtenders.gov.in/nicgep",
            "https://govtprocurement.delhi.gov.in/nicgep",
            "https://jktenders.gov.in/nicgep",
            "https://tenders.ladakh.gov.in/nicgep",
            "https://tendersutl.gov.in/nicgep",
            "https://pudutenders.gov.in/nicgep",
        ]

        try:
            for index, state in enumerate(states):
                print(f"\nProcessing ({index}): {state}")
                try:
                    url = f"{state}/app?page=FrontEndTendersByOrganisation&service=page"
                    url_name = "/".join(state.split("/")[:3])
                    html_page = requests.get(url)
                    self.extract_data(html_page, url_name)
                    self.run2(url_name)

                    if len(self.tmp_collected_data) != 0:
                        self.run3()
                    else:
                        print(f"No Data to scrape in {url_name}")

                except Exception as e:
                    print(f"Unable to scrape {state}\n{traceback.print_exc()}")
        except Exception as e:
            print(
                f"Error occurred. Closing scraping process.\n{str(e)}",
                traceback.print_exc(),
            )
        finally:
            self.save_data()
            sys.exit()


def main():
    config = load_config_yaml()["paths"]["ETENDERSINDIA"]
    eTendersIndiaMetadataScraper(config=config).run()


if __name__ == "__main__":
    mn = main()
