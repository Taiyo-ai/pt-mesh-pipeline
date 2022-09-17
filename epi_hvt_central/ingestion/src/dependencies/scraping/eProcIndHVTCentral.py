import traceback
from multiprocessing import Pool

import pandas as pd
from tqdm import tqdm

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from chromedriver_py import binary_path

from ..scraping import BaseScraper
from ..utils import load_config_yaml
from ..utils.bucket import (
    push_csv_to_buffer_bucket,
    read_csv_from_buffer_bucket,
)


class EPIHighValueTendersCentralScraper(BaseScraper):
    def __init__(self, **kwargs):
        """
        Keyword Arguments:
        ------------------------------------------------------------------------
            config:
            - The configuration dictionary with relative paths to AWS/GCS
              buckets. These paths are used to modify the metadata and store the
              data for all the intermediate processes.
        """
        self.config: dict = kwargs.get("config")
        self.collected_data = []
        super().__init__()

    def find_number_of_pages(self, url: str):
        """
        Finds the total number tenders and finds the numbers of pages
        over which tenders data is distributed

        =================================================================

        ### Input Arguments:
        url: URL of the page

        ### Returns: (total_number_of_tenders, total_pages)
        total_number_of_tenders: Total number of tenders found
        total_pages: Total number of pages found in pagination
        """
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, "lxml")

        total_number_of_tenders = (
            soup.find("div", {"id": "edit-data4"}).find("div").text
        )
        total_number_of_tenders = eval(total_number_of_tenders.split(":")[1].strip())
        print(f"Total Number of Active Tenders found: {total_number_of_tenders}")

        total_pages = eval(
            soup.find("div", {"class": "pagination"})
            .findAll("a", {"class": "paginate_button"})[-2]
            .text
        )
        print(f"Total Number of Pages found: {total_pages}\n")
        return total_number_of_tenders, total_pages

    def create_list_of_urls(self, sample_url: str, total_pages: int) -> list:
        """
        Generates list of URLs

        =================================================================

        ### Input Arguments:
        sample_url: URL from which the list has to be generated
        total_pages: Total number of pages

        ### Returns:
        url_list: List of URLs
        """
        url_list = []
        for page_num in range(1, total_pages + 1):
            url = f"{sample_url}?page={page_num}"
            url_list.append(url)
        return url_list

    @staticmethod
    def extract_data(page_url: str):
        """
        Extract data from individual pages

        =====================================================================

        Input Arguments:
        ---------------------------------------------------------------------
        page_url
            - URL of the page

        driver_config
            - Selenium webdriver configuration

        Returns:
        ---------------------------------------------------------------------
        Dictionary with data scraped from the page and bool object which
        tells whether the data was successfully scraped or not
        """

        def add_driver_options(options):
            """
            Add configurable options
            """
            chrome_options = Options()
            for opt in options:
                chrome_options.add_argument(opt)
            return chrome_options

        def initialize_driver():
            """
            Initialize the web driver
            """
            driver_config = {
                "executable_path": binary_path,
                "options": [
                    "--headless",
                    "--no-sandbox",
                    "--start-fullscreen",
                    "--allow-insecure-localhost",
                    "--disable-dev-shm-usage",
                ],
            }
            options = add_driver_options(driver_config["options"])
            driver = webdriver.Chrome(
                executable_path=driver_config["executable_path"], options=options
            )
            return driver

        def number_of_rows_to_iterate(url: str) -> int:
            """
            Finds the number of tenders on a particular page

            =================================================================

            ### Input Arguments:
            url: URL from which the list has to be generated

            ### Returns:
            num_rows: Number of items present
            """

            resp = requests.get(url)
            soup = BeautifulSoup(resp.text, "lxml")
            table = soup.find("table", {"class": "list_table"})
            num_rows = len(table.findAll("tr"))
            print(f"\n{num_rows-1} items found")
            return num_rows

        driver = initialize_driver()
        driver.get(page_url)

        collected_data = []
        result = {"page_data": collected_data, "success": False}
        try:
            WebDriverWait(driver, 60).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//table[@class='list_table']")
                )
            )

            num_rows = number_of_rows_to_iterate(page_url)
            for i in tqdm(range(1, num_rows)):
                page_data = {
                    "tender_reference_number": "",
                    "title": "",
                    # "status": "Active",
                    # Critical Dates
                    "epublished_date": "",
                    "epublished_date_": "",
                    "tender_opening_date": "",
                    "bid_opening_date": "",
                    "bid_submission_start_date": "",
                    "bid_submission_closing_date": "",
                    "bid_submission_end_date": "",
                    "document_download_start_date": "",
                    "document_download_end_date": "",
                    # Tender Details
                    "organization_name": "",
                    "organization_type": "",
                    "tender_type": "",
                    "tender_category": "",
                    "product_category": "",
                    "product_sub_category": "",
                    "tender_fee": "",
                    "emd": "",
                    "location": "",
                    "state_name": "",
                    "work_description": "",
                    "corrigendum": "",
                    # Authority Details
                    "inviting_authority_name": "",
                    "inviting_authority_address": "",
                    # URL
                    "tender_document_link": "",
                    "sessioned_url": "",
                }

                page_data["epublished_date"] = driver.find_element_by_xpath(
                    f"//*[@id='table']/tbody/tr[{i}]/td[2]"
                ).text.strip()
                page_data["bid_submission_closing_date"] = driver.find_element_by_xpath(
                    f"//*[@id='table']/tbody/tr[{i}]/td[3]"
                ).text.strip()
                page_data["tender_opening_date"] = driver.find_element_by_xpath(
                    f"//*[@id='table']/tbody/tr[{i}]/td[4]"
                ).text.strip()
                page_data["title"] = driver.find_element_by_xpath(
                    f"//*[@id='table']/tbody/tr[{i}]/td[5]/a"
                ).text.strip()
                page_data["sessioned_url"] = driver.find_element_by_xpath(
                    f"//*[@id='table']/tbody/tr[{i}]/td[5]/a"
                ).get_attribute("href")
                page_data["organization_name"] = driver.find_element_by_xpath(
                    f"//*[@id='table']/tbody/tr[{i}]/td[6]"
                ).text.strip()
                page_data["corrigendum"] = driver.find_element_by_xpath(
                    f"//*[@id='table']/tbody/tr[{i}]/td[7]"
                ).text.strip()

                link_path = f'//*[@id="table"]/tbody/tr[{i}]/td[5]/a'
                # print(driver.find_element_by_xpath(path).text)
                driver.find_element_by_xpath(link_path).click()

                # Fill in the CAPTCHA
                wait = WebDriverWait(driver, 60)
                captcha = wait.until(
                    EC.visibility_of_element_located(
                        (By.XPATH, "//img[@title='Image CAPTCHA']")
                    )
                )
                scaptcha_text = captcha.get_attribute("alt")
                driver.find_element_by_xpath(
                    "//input[@id='edit-captcha-response']"
                ).send_keys(scaptcha_text)
                driver.find_element_by_id("edit-save").click()

                wait.until(
                    EC.visibility_of_element_located((By.XPATH, "//*[@id='tfullview']"))
                )
                tender_page = BeautifulSoup(driver.page_source, "lxml")
                tables = tender_page.findAll("table", {"width": "100%"})

                page_data["organization_type"] = (
                    tables[0].findAll("tr")[1].find("div").text.strip()
                )

                page_data["tender_reference_number"] = (
                    tables[1]
                    .findAll("tr")[1]
                    .findAll("td", {"width": "20%"})[0]
                    .text.strip()
                )
                page_data["tender_type"] = (
                    tables[1]
                    .findAll("tr")[1]
                    .findAll("td", {"width": "20%"})[1]
                    .text.strip()
                )
                page_data["tender_category"] = (
                    tables[1]
                    .findAll("tr")[2]
                    .findAll("td", {"width": "20%"})[0]
                    .text.strip()
                )
                page_data["product_category"] = (
                    tables[1]
                    .findAll("tr")[2]
                    .findAll("td", {"width": "20%"})[1]
                    .text.strip()
                )
                page_data["product_sub_category"] = (
                    tables[1]
                    .findAll("tr")[3]
                    .findAll("td", {"width": "20%"})[0]
                    .text.strip()
                )
                page_data["tender_fee"] = (
                    tables[1]
                    .findAll("tr")[3]
                    .findAll("td", {"width": "20%"})[1]
                    .text.strip()
                )
                page_data["emd"] = (
                    tables[1]
                    .findAll("tr")[4]
                    .findAll("td", {"width": "20%"})[0]
                    .text.strip()
                )
                page_data["location"] = (
                    tables[1]
                    .findAll("tr")[4]
                    .findAll("td", {"width": "20%"})[1]
                    .text.strip()
                )

                page_data["epublished_date_"] = (
                    tables[2]
                    .findAll("tr")[0]
                    .findAll("td", {"width": "20%"})[0]
                    .text.strip()
                )
                page_data["bid_opening_date"] = (
                    tables[2]
                    .findAll("tr")[0]
                    .findAll("td", {"width": "20%"})[1]
                    .text.strip()
                )
                page_data["document_download_start_date"] = (
                    tables[2]
                    .findAll("tr")[1]
                    .findAll("td", {"width": "20%"})[0]
                    .text.strip()
                )
                page_data["document_download_end_date"] = (
                    tables[2]
                    .findAll("tr")[1]
                    .findAll("td", {"width": "20%"})[1]
                    .text.strip()
                )
                page_data["bid_submission_start_date"] = (
                    tables[2]
                    .findAll("tr")[2]
                    .findAll("td", {"width": "20%"})[0]
                    .text.strip()
                )
                page_data["bid_submission_end_date"] = (
                    tables[2]
                    .findAll("tr")[2]
                    .findAll("td", {"width": "20%"})[1]
                    .text.strip()
                )

                page_data["work_description"] = (
                    tables[3].findAll("tr")[0].find("div").text.strip()
                )
                page_data["tender_document_link"] = (
                    tables[3].findAll("tr")[1].find("div").text.strip()
                )

                page_data["inviting_authority_name"] = (
                    tables[4].findAll("tr")[0].find("div").text.strip()
                )
                page_data["inviting_authority_address"] = (
                    tables[4].findAll("tr")[1].find("div").text.strip()
                )

                # back to CAPTCHA security page
                driver.back()
                wait.until(
                    EC.visibility_of_element_located(
                        (By.XPATH, "//img[@title='Image CAPTCHA']")
                    )
                )

                # back to tender search results page
                driver.back()
                wait.until(
                    EC.visibility_of_element_located(
                        (By.XPATH, "//table[@class='list_table']")
                    )
                )

                # Consolidating Data
                collected_data.append(page_data)

            result = {"page_data": collected_data, "success": True}

        except Exception as e:
            # driver.quit()
            print(
                f"Error occured while scraping page {page_url}\n{e}",
                traceback.print_exc(),
            )
        finally:
            driver.quit()
            return result

    def load_data(self, master_data_path: str = ""):
        try:
            self.master_df = read_csv_from_buffer_bucket(self.bucket, master_data_path)
        except Exception as e:
            print(f"Error occurred while loading data\n{str(e)}")
            pass

    def save_data(self, master_data_path: str, drop_dups_cols: list = None):
        if drop_dups_cols is None:
            drop_dups_cols = ["project_id"]
        if self.master_df is None:
            self.master_df = pd.DataFrame(self.collected_data)
        else:
            self.master_df = self.master_df.append(
                self.collected_data, ignore_index=True
            )
        self.master_df.drop_duplicates(drop_dups_cols, keep="last", inplace=True)
        push_csv_to_buffer_bucket(self.bucket, self.master_df, master_data_path)

    def run(self):
        try:
            self.load_data(self.config["epihvt_master_data_path"])

            URL = "https://eprocure.gov.in/cppp/highvaluetenders/cpppdata"
            _, total_pages = self.find_number_of_pages(URL)
            url_list = self.create_list_of_urls(URL, total_pages)

            with Pool(processes=self.config["PROCESSES"]) as pool:
                final_result = pool.map(self.extract_data, url_list)
                pool.close()
                pool.join()

            for result in final_result:
                if result["success"]:
                    self.collected_data.extend(result["page_data"])
        except Exception as e:
            print(
                f"Error occurred. Closing scraping process.\n{str(e)}",
                traceback.print_exc(),
            )
        finally:
            self.save_data(
                self.config["epihvt_master_data_path"], self.config["drop_duplicates"]
            )


if __name__ == "__main__":
    path_config = load_config_yaml()["paths"]["EPIHVTC"]
    config = {
        "PROCESSES": 7,
        "executable_path": "/usr/bin/chromedriver",
        "options": [
            "--headless",
            "--no-sandbox",
            "--start-fullscreen",
            "--allow-insecure-localhost",
            "--disable-dev-shm-usage",
        ],
        "drop_duplicates": ["tender_reference_number"],
        "epihvt_master_data_path": path_config["master_data_path"],
    }

    scraper = EPIHighValueTendersCentralScraper(config=config)
    scraper.run()
