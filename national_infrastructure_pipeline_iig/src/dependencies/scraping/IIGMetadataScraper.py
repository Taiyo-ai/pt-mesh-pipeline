import traceback
import pandas as pd
import time
import random

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from chromedriver_py import binary_path

from ..utils import load_config_yaml
from ..utils.bucket import (
    connect_to_buffer_bucket,
    push_csv_to_buffer_bucket,
)


class IIGMetadataScraper:
    def __init__(self, **kwargs):
        self.page_url_list = []
        self.collected_data = []
        self.meta_data = None
        self.config = kwargs.get("config")
        self.bucket = None
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--start-fullscreen")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--allow-insecure-localhost")
        self.browser = webdriver.Chrome(
            executable_path=binary_path,
            options=chrome_options,
        )

    def scroll(self):

        # Set randomized timeouts to prevent getting blocked
        scroll_pause_time = random.randint(5, 10)

        # Get scroll height
        last_height = self.browser.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            self.browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )

            # Wait to load page
            time.sleep(scroll_pause_time)

            # Calculate new scroll height and compare with last scroll height
            new_height = self.browser.execute_script(
                "return document.body.scrollHeight"
            )
            if new_height == last_height:
                # If heights are the same it will exit the function
                break
            last_height = new_height

    def extract_data(self, url):

        result = {"success": False, "page_data": []}
        try:
            self.browser.get(url)
            time.sleep(10)
            self.scroll()
            data = self.browser.page_source
            HTMLPage = BeautifulSoup(data, "html.parser")
            project_wrapper = HTMLPage.find_all("section", class_="dg-project-cards")
            enum = url.split("/")[4]
            enum = enum[: len(enum) - 1]
            sector = url.split("/")[5].split("?")[0]
            array = []
            for wrapper in project_wrapper:
                projects = wrapper.find_all("div", class_=["card-body"])
                projects = [projects[i] for i in range(len(projects)) if i % 2 != 0]

                for project in projects:
                    obj = {
                        "project_id": "",
                        "project_title": "",
                        "project_investment": "",
                        "project_address": "",
                        "url": "",
                        "type": "",
                        "sub_sector": "",
                        "sector": "",
                    }

                    try:
                        project_id = (
                            project.find("p", class_="project-id")
                            .text.strip()
                            .replace("Project ID: ", "")
                            .strip()
                        )
                        project_id = project_id[project_id.find(":") + 1 :].strip()
                        obj["project_id"] = project_id
                        obj["project_title"] = project.find(
                            "h3", class_="card-main-project-title"
                        ).text.strip()

                        obj["type"] = enum
                        obj["sector"] = sector
                        obj["project_investment"] = (
                            project.find("h3", class_="card-project-number")
                            .text.strip()
                            .replace("\n", " ")
                        )
                        obj["project_address"] = (
                            project.find("div", class_="card-project-address")
                            .find_all("span")[0]
                            .text.replace("State(s) | ", "")
                            .strip()
                        )
                        obj["sub_sector"] = (
                            project.find("div", class_="card-project-address")
                            .find_all("span")[1]
                            .text.replace("Sub-sector | ", "")
                            .strip()
                        )
                        obj["url"] = (
                            "https://indiainvestmentgrid.gov.in/opportunities/"
                            + enum
                            + "/"
                            + str(obj["project_id"])
                        )
                    except Exception as e:
                        print(f"Error getting Page Data from url: {url}:\n{e}")
                        pass
                    array.append(obj)
            result = {"success": True, "page_data": array}
            print(f"Successfuly scraped url: {url}")
            return result
        except Exception as e:
            print(f"Error getting Page Data from url: {url}:\n{e}")
            return result

    def create_page_url_list(self):
        # enum = ["nip-projects", "projects", "stressed-assets", "csr-projects"]
        enum = ["nip-projects", "projects"]
        for type in enum:

            BASE_URL = f"https://indiainvestmentgrid.gov.in/opportunities/{type}"

            try:
                self.browser.get(BASE_URL)
                time.sleep(10)
                data = self.browser.page_source
                HTMLPage = BeautifulSoup(data, "html.parser")

                # Get list of acitve sectors for the particular project type
                sector_list_wrapper = HTMLPage.find("ul", class_="search-list")
                active_sectors = sector_list_wrapper.find_all(
                    "li", {"class": ["active"]}
                )

                # Make a list of all the available sectors and sub-sectors to create a url
                sector_list = []
                for sector in active_sectors:
                    obj = {"sector": "", "sub_sector": []}
                    try:
                        obj["sector"] = (
                            sector.div.text.strip()
                            .lower()
                            .replace(" ", "-")
                            .replace("&", "and")
                        )
                        for sub_sector in sector.find_all("li", class_="active"):
                            obj["sub_sector"].append(
                                {
                                    "name": sub_sector.text.strip(),
                                    "data-id": sub_sector.get("data-id"),
                                }
                            )
                        sector_list.append(obj)

                    except Exception as e:
                        print(f"Error getting Sector-sub Sector list:\n{e}")
                        pass
                urls = []
                url = ""
                TEMPLATE_URL = (
                    f"https://indiainvestmentgrid.gov.in/opportunities/{type}/"
                )
                for sector_obj in sector_list:
                    for sub_sector in sector_obj["sub_sector"]:
                        data_id = str(sub_sector["data-id"])
                        url = (
                            TEMPLATE_URL
                            + sector_obj["sector"]
                            + "?subSector="
                            + data_id
                            + "&all=1"
                        )
                        urls.append(url)
                self.page_url_list += urls

            except Exception as e:
                print(f"Error generating URL list for different pages:\n{e}")

    def save_data(self):
        try:
            self.bucket = connect_to_buffer_bucket()
            self.meta_data = pd.DataFrame(self.collected_data)
            # self.meta_data.to_csv('uspermits_base_data.csv',index=False)
            push_csv_to_buffer_bucket(
                self.bucket, self.meta_data, self.config["base_data_path"]
            )

            project_urls = self.meta_data.loc[:, ["project_id", "url"]]
            # project_urls.to_csv('project_ids_urls.csv',index=False)
            push_csv_to_buffer_bucket(
                self.bucket, project_urls, self.config["reference_urls_path"]
            )
        except Exception as e:
            print(f"Error occurred while saving data.\n{str(e)}", traceback.print_exc())

    def run(self):
        self.create_page_url_list()
        try:

            final_result = []
            for url in self.page_url_list:
                final_result.append(self.extract_data(url))
            for result in final_result:
                if result["success"]:
                    self.collected_data.extend(result["page_data"])
                else:
                    print("Failed getting page data")
        except Exception as e:
            print(
                f"Error occurred. Closing scraping process.\n{str(e)}",
                traceback.print_exc(),
            )
        finally:
            self.save_data()


if __name__ == "__main__":
    path_config = load_config_yaml()["paths"]["IIG"]
    config = {
        "options": [
            "--headless",
            "--start-fullscreen",
            "--no-sandbox",
            "--allow-insecure-localhost",
        ],
        "master_data_path": path_config["master_data_path"],
        "successful_urls_path": path_config["successful_urls_path"],
        "failed_urls_path": path_config["failed_urls_path"],
        "reference_urls_path": path_config["reference_urls_path"],
        "base_data_path": path_config["base_data_path"],
    }
    IIGMetadataScraper(config=config).run()
