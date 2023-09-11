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

        page_data = {
            "description": "",
            "project_id": row[0],
            "url": row[1],
            "sector": "",
            "location": [],
            "funding_requirement": "",
            "funding_details": "",
            "sub-sector": "",
        }
        result = {"page_data": page_data, "success": False}

        try:
            self.driver.get(row[1])
            time.sleep(5)
            data = self.driver.page_source
            HTMLPage = BeautifulSoup(data, "html.parser")

            try:
                heading = HTMLPage.find("div", {"id": "contentPrintHeading"})
                title = heading.h1.text.strip()
                page_data["project_title"] = title
                last_update = heading.find_all("small")[-1].b.text.strip()
                page_data["last_updated"] = last_update
            except Exception as e:
                pass

            try:
                page_data["description"] = HTMLPage.find(
                    "div", class_="project-details-section"
                ).p.text.strip()
            except Exception as e:
                pass

            try:
                address = []
                address_wrapper = HTMLPage.find("div", class_="all-adress")
                listed_addresses = address_wrapper.find_all("p", class_="address")
                address = [w.text.strip() for w in listed_addresses]
                page_data["location"] = address
            except Exception as e:
                pass

            try:
                details = HTMLPage.find("div", class_="snapshot-details-wrapper")
                for item in details.find_all("li"):
                    page_data[item.h6.text.strip().lower()] = item.span.text.lower()
            except Exception as e:
                pass

            try:
                financial = HTMLPage.find("div", class_="csr-project-funding-card")
                req = financial.find("li")
                page_data["funding_requirement"] = (
                    req.span.text.strip().lower().replace("\xa0", "")
                )
            except Exception as e:
                pass

            try:
                area_tags = HTMLPage.find("div", class_="csr-areas-tags-main")
                page_data["funding_details"] = area_tags.find("li").text.strip()
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
            print(self.scraping_list_df)
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
    path_config = load_config_yaml()["paths"]["IIG_CSR"]
    config = {
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
