import traceback

import math
import pandas as pd
from tqdm import tqdm

import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException

from chromedriver_py import binary_path

from ..scraping import BaseScraper
from ..utils import load_config_yaml
from ..utils.bucket import (
    push_csv_to_buffer_bucket,
    read_csv_from_buffer_bucket,
)


class EPICancelledStateScraper(BaseScraper):
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
        self.URL = "https://eprocure.gov.in/cppp/cancelledtenders/mmpdata"
        super().__init__(self.config["options"], self.config["executable_path"])

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
        print(f"Total Number of Cancelled Tenders found: {total_number_of_tenders}")

        total_pages = math.ceil(total_number_of_tenders / 10)
        print(f"Total Number of Pages found: {total_pages}\n")
        return total_number_of_tenders, total_pages

    def extract_data(self, driver: webdriver, year: str, scrape_pages: int = None):
        driver.get(self.URL)

        select = Select(driver.find_element_by_id("edit-m-year"))
        select.select_by_value(year)

        captcha_text = driver.find_element_by_xpath(
            "//img[@title='Image CAPTCHA']"
        ).get_attribute("alt")
        driver.find_element_by_xpath("//input[@id='edit-captcha-response']").send_keys(
            captcha_text
        )
        driver.find_element_by_id("btnSearch").click()

        wait = WebDriverWait(driver, 60)
        wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[@id='tenderscpppdata_short-div']")
            )
        )

        _, total_pages = self.find_number_of_pages(driver.current_url)
        if scrape_pages is None:
            num_pages = total_pages
        else:
            num_pages = scrape_pages

        for page in tqdm(range(num_pages)):
            table = BeautifulSoup(driver.page_source, "lxml").find("tbody")

            for i in tqdm(range(1, len(table.findAll("tr")) + 1)):
                page_data = {
                    "tender_reference_number": "",
                    "title": "",
                    "status": "",
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
                page_data["state_name"] = driver.find_element_by_xpath(
                    f"//*[@id='table']/tbody/tr[{i}]/td[6]"
                ).text.strip()
                page_data["status"] = driver.find_element_by_xpath(
                    f"//*[@id='table']/tbody/tr[{i}]/td[7]"
                ).text.strip()

                # Visting every tenders page to collect data
                link_path = f'//*[@id="table"]/tbody/tr[{i}]/td[5]/a'
                driver.find_element_by_xpath(link_path).click()

                # Fill in the CAPTCHA
                wait = WebDriverWait(driver, 60)
                # captcha = wait.until(
                #     EC.visibility_of_element_located((By.XPATH,"//img[@title='Image CAPTCHA']"))
                # )
                # scaptcha_text = captcha.get_attribute('alt')
                # driver.find_element_by_xpath("//input[@id='edit-captcha-response']").send_keys(scaptcha_text)
                # driver.find_element_by_id("edit-save").click()

                # Waiting the data to be visible
                wait.until(
                    EC.visibility_of_element_located(
                        (By.XPATH, "//*[@id='tender_full_view']")
                    )
                )
                tender_page = BeautifulSoup(driver.page_source, "lxml")
                tables = tender_page.findAll("table", {"width": "100%"})

                page_data["organization_name"] = (
                    tables[0].findAll("tr")[0].find("div").text.strip()
                )
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

                # Consolidating the tenders data
                self.add_to_collected_data(page_data)

                # Going back to page with table
                # driver.back()
                # wait.until(
                #     EC.visibility_of_element_located((By.XPATH,"//img[@title='Image CAPTCHA']"))
                # )

                # back to tender search results page
                driver.back()
                wait.until(
                    EC.visibility_of_element_located(
                        (By.XPATH, "//table[@class='list_table']")
                    )
                )

            # Go to next page
            try:
                next_page_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.LINK_TEXT, "Next »"))
                )
                next_page_button.click()
                wait.until(
                    EC.visibility_of_element_located(
                        (By.XPATH, "//table[@class='list_table']")
                    )
                )
            except WebDriverException as e:
                print("\nReached the last page. Scraping will end successfully soon")
                pass

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
            self.load_data(
                self.config["epictc_master_data_path"].replace(
                    "<year>", self.config["year"]
                )
            )
            self.extract_data(self.driver, self.config["year"], None)
        except Exception as e:
            print(
                f"Error occurred. Closing scraping process.\n{str(e)}",
                traceback.print_exc(),
            )
        finally:
            self.driver.close()
            self.save_data(
                self.config["epictc_master_data_path"].replace(
                    "<year>", self.config["year"]
                ),
                self.config["drop_duplicates"],
            )


if __name__ == "__main__":
    path_config = load_config_yaml()["paths"]["EPICANS"]
    config = {
        "executable_path": binary_path,
        "options": [
            "--headless",
            "--no-sandbox",
            "--start-fullscreen",
            "--allow-insecure-localhost",
            "--disable-dev-shm-usage",
        ],
        "drop_duplicates": ["tender_reference_number"],
        "year": "2021",
        "epictc_master_data_path": path_config["master_data_path"],
    }

    scraper = EPICancelledStateScraper(config=config)
    scraper.run()
