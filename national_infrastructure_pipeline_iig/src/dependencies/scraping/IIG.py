import os
import traceback
import time
import pandas as pd

from bs4 import BeautifulSoup
from chromedriver_py import binary_path

from ..scraping import BaseScraper
from ..utils import load_config_yaml
from ..utils.bucket import read_csv_from_buffer_bucket


class IIGScraper(BaseScraper):
    def __init__(self, config):
        self.url = None
        self.config = config
        self.retry = 5
        super().__init__(
            driver_options=config["options"],
            driver_executable_path=binary_path,
        )

    def extract_data(self, row):
        print(row[1])

        page_data = {
            "project_id": "",
            "project_title": "",
            "project_status": "",
            "country": "India",
            "sector": "",
            "sub_sector": "",
            "project_start_date": "",
            "project_completion_date": "",
            "last_updated_date": "",
            "stage": "",
            "views": "",
            "url": row[1],
            "requirement_type": "",
            "requirement_details": "",
            "line_ministry": "",
            "address": "",
            "promoter_type": "",
            "investment_in_usd": "",
            "state": "",
        }
        result = {"page_data": page_data, "success": False}

        try:
            self.driver.get(row[1])
            time.sleep(5)
            # data = request.urlopen("https://indiainvestmentgrid.gov.in/opportunities/nip-project/701693").read()
            data = self.driver.page_source
            HTMLPage = BeautifulSoup(data, "html.parser")
            try:
                page_data["views"] = HTMLPage.find(
                    "div", class_="right-side-view"
                ).span.text.strip()
            except Exception as e:
                pass

            try:
                page_data["project_title"] = HTMLPage.find(
                    "h1", class_="prj-name"
                ).text.strip()
            except Exception as e:
                pass

            try:
                page_data["project_id"] = (
                    HTMLPage.find("div", class_="projectIdSection")
                    .h6.text.replace("Project ID:", "")
                    .strip()
                )
            except Exception as e:
                pass

            try:
                page_data["address"] = HTMLPage.find("p", class_="address").text
            except Exception as e:
                pass

            try:
                last_updated = (
                    HTMLPage.find("div", class_="last-date")
                    .text.strip()
                    .replace("\r", "")
                    .replace("\n", "")
                    .replace("\t", "")
                )
                last_updated = last_updated[last_updated.find(":") + 1 :]
                page_data["last_updated_date"] = last_updated
            except Exception as e:
                pass

            try:
                stage = HTMLPage.find_all("div", class_="active-stage")[-1].text.strip()
                page_data["stage"] = stage
            except Exception as e:
                pass

            try:
                page_data["investment_in_usd"] = HTMLPage.find(
                    "span", class_="total-cost-value"
                ).text.strip()
            except Exception as e:
                pass

            try:
                details = HTMLPage.find_all("div", "details-wrapper")
                for detail in details:
                    page_data[
                        detail.h6.text.strip()
                        .lower()
                        .replace(" ", "_")
                        .replace("-", "_")
                    ] = detail.span.text.strip().replace("-", "")
            except Exception as e:
                pass

            try:
                project_req_wrapper = HTMLPage.find("div", class_="prjrequirement-body")
                reqs = project_req_wrapper.find_all("div", class_="form-group")
                for requirement in reqs:
                    page_data[
                        requirement.label.text.strip().lower().replace(" ", "_")
                    ] = requirement.span.text.strip()
            except Exception as e:
                pass

            print(f"Scrapped page {page_data['url']} successfully\n")

            # consolidating data
            result = {"page_data": page_data, "success": True}

        except Exception as e:
            print(f"Error occurred for page  {page_data['url']}\n{str(e)}")
        finally:
            return result

    def run(self):
        self.load_data(
            reference_urls_path=self.config["iig_urls_path"],
            master_data_path=self.config["iig_data_path"],
            success_urls_path=self.config["iig_success_urls_path"],
            failed_urls_path=self.config["iig_failed_urls_path"],
        )

        try:
            final_result = []
            print(len(self.scraping_list_df.values.tolist()))
            for row in self.scraping_list_df.values.tolist():
                final_result.append(self.extract_data(row))
            for result in final_result:
                if result["success"]:
                    self.add_to_collected_data(result["page_data"])
                    self.add_url_to_success_list(
                        result["page_data"]["project_id"],
                        result["page_data"]["url"],
                    )
                else:
                    self.add_url_to_failed_list(
                        result["page_data"]["project_id"],
                        result["page_data"]["url"],
                    )

        except Exception as e:
            print(
                f"Error occurred. Closing scraping process.\n{str(e)}",
                traceback.print_exc(),
            )

        finally:
            self.driver.quit()
            self.save_data(
                master_data_path=self.config["iig_data_path"],
                success_urls_path=self.config["iig_success_urls_path"],
                failed_urls_path=self.config["iig_failed_urls_path"],
                drop_dups_cols=None,
            )


if __name__ == "__main__":
    path_config = load_config_yaml()["paths"]["IIG"]
    config = {
        "executable_path": "src/ppp_scrapers/scrapers/chromedriver/chromedriver.exe",
        "options": [
            "--headless",
            "--start-fullscreen",
            "--no-sandbox",
            "--allow-insecure-localhost",
        ],
        "iig_urls_path": path_config["reference_urls_path"],
        "iig_success_urls_path": path_config["successful_urls_path"],
        "iig_failed_urls_path": path_config["failed_urls_path"],
        "iig_data_path": path_config["master_data_path"],
    }

    scraper = IIGScraper(config)
    scraper.run()
