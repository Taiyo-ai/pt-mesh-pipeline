import os
import traceback
import time
import pandas as pd

import requests
from bs4 import BeautifulSoup
from chromedriver_py import binary_path

from ..scraping import BaseScraper
from ..utils import load_config_yaml
from ..utils.bucket import read_csv_from_buffer_bucket


class IIGAssetsScraper(BaseScraper):
    def __init__(self, config):
        self.url = None
        self.config = config
        self.retry = 5
        print("Downloaded")
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
            "company type": "",
            "type": "",
            "employees": "",
            "register address": "",
            "website": "",
            "key products/services": "",
            "key resources/assets": "",
            "commencement of cirp": "",
            "public announcement by resolution professional": "",
            "claim submission": "",
            "invitation for expression of interest": "",
            "submission of expression of interest": "",
            "submission of resolution plan": "",
            "committee of creditors approval": "",
            "submission of resolution plan to nclt": "",
            "approval of resolution plan by nclt": "",
            "Opportunity Highlights": "-",
            "Amount": "",
            "links": [],
        }
        result = {"page_data": page_data, "success": False}

        try:
            self.driver.get(row[1])
            time.sleep(5)
            data = self.driver.page_source
            HTMLPage = BeautifulSoup(data, "html.parser")

            try:
                title_wrapper = HTMLPage.find("div", class_="page-details-inner")
                page_data["project_name"] = title_wrapper.find("h1").text.strip()
            except Exception as e:
                pass

            try:
                card_wrapper = HTMLPage.find("section", {"id": "ProjectSpecification"})
                card_body = card_wrapper.find("div", class_="card-body")
                rows = card_body.find_all("div", class_="form-group")
                for item in rows:
                    page_data[
                        item.div.text.strip().lower()
                    ] = item.span.text.strip().lower()
            except Exception as e:
                pass

            try:
                timeline_entries = HTMLPage.find_all("article", class_="timeline-entry")
                year = HTMLPage.find("span", class_="digi-card-year").text.strip()
                for timeline in timeline_entries:
                    date = timeline.find("div", class_="timeline-time").find_all("span")
                    date = " ".join([x.text.strip() for x in date]) + " " + year
                    page_data[
                        timeline.find("div", class_="timeline-label")
                        .text.strip()
                        .lower()
                    ] = date
            except Exception as e:
                pass

            try:
                accordion = HTMLPage.find("div", class_="dg_accordion")
                acc_cards = accordion.find_all("div", class_="form-group")
                for card in acc_cards:
                    try:
                        page_data[card.label.text.strip()] = card.span.text.strip()
                    except Exception as e:
                        pass
            except Exception as e:
                pass

            try:
                link_list = HTMLPage.find_all("li", class_="list-unstyled")
                links = []
                for link in link_list:
                    links.append(link.a.get("href"))
                page_data["links"] = links
            except Exception as e:
                pass

            try:
                last_updated = (
                    title_wrapper.find_all("small")[-1]
                    .find("b")
                    .text.replace("\t", "")
                    .replace("\n", "")
                    .replace("'", "")
                    .strip()
                )
                page_data["last_updated_date"] = last_updated
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

            try:
                table = HTMLPage.find("table", class_="table")
                header_row = table.find_all("tr")[0]
                headers = []
                for th in header_row.find_all("th")[1:]:
                    headers.append(th.text)
                for row in table.find_all("tr")[1:]:
                    year = row.find("th").text.strip()
                    for i in range(len(headers)):
                        page_data[headers[i] + "_" + year] = row.find_all("td")[
                            i
                        ].text.strip()
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
            print(len(list(self.scraping_list_df["url"])))
            for row in self.scraping_list_df.values.tolist()[:500]:
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

    def download(self):
        df = read_csv_from_buffer_bucket(self.bucket, self.config["iig_data_path"])
        df.to_csv("iig_assets.csv", index=False)


if __name__ == "__main__":
    path_config = load_config_yaml()["paths"]["IIG_Assets"]
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

    scraper = IIGAssetsScraper(config)
    scraper.run()
