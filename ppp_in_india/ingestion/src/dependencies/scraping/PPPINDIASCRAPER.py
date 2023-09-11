import sys
import bs4

from ..scraping import BaseScraper
from ..utils import load_config_yaml


class PPPINDIAScraper(BaseScraper):
    def __init__(self, config):
        self.project_count = 0
        self.config = config

        super().__init__(None, None)

    def extract_data(self, project_id, url):
        page_data = {
            "project_id": project_id,
            "project_name": "",
            "url": url,
            "type": "",
            "project_capacity": "",
            "project_cost": "",
            "sector": "",
            "sub_sector": "",
            "status": "",
            "project_authority": "",
            "date_of_award": "",
            "location": "",
            "update_date": "",
        }

        try:
            html = self.get_html_for_url(url)
            soup = bs4.BeautifulSoup(html, "lxml")
            table = soup.findAll("tbody")[0].findAll("tbody")[0]
            rows = table.findAll("tr")

            # Row 0
            row_0_cells = rows[0].findAll("td")
            page_data["project_name"] = self.get_element_value(
                row_0_cells[1], "strong", "Name"
            )
            page_data["type"] = self.get_element_value(row_0_cells[2], "strong", "type")
            page_data["project_capacity"] = self.get_element_value(
                row_0_cells[3], "strong", "project capacity"
            )

            # Row 1
            row_1_cells = rows[1].findAll("td")
            page_data["sector"] = self.get_element_value(
                row_1_cells[0], "strong", "Sector"
            )
            page_data["sub_sector"] = row_1_cells[1].find("span").text.strip()
            page_data["status"] = self.get_element_value(
                row_1_cells[3], "strong", "status"
            )

            # Row 2
            row_2_cells = rows[2].findAll("td")

            page_data["total_project_cost"] = self.get_element_value(
                row_2_cells[0], "strong", "Total cost"
            )
            page_data["project_authority"] = self.get_element_value(
                row_2_cells[0], "strong", "Project Authority"
            )

            page_data["date_of_award"] = self.get_element_value(
                row_2_cells[2], "strong", "Date of Award"
            )
            page_data["location"] = self.get_element_value(
                row_2_cells[3], "strong", "Location"
            )
            page_data["updated_date"] = self.get_element_value(
                row_2_cells[3], "strong", "Updated Date"
            )
            # consolidating data
            print(
                f"Scrapped below information for url ({self.project_count + 1}): {url}"
            )
            self.add_to_collected_data(page_data)
            self.add_url_to_success_list(project_id, url)

        except Exception as e:
            print(f"Error occurred for url ({self.project_count + 1}): {url}\n{str(e)}")
            self.add_url_to_failed_list(project_id, url)
        finally:
            self.project_count += 1

    @staticmethod
    def get_element_value(obj, tag, ele_text, strip_list=None):
        value = ""
        strip_list = strip_list if strip_list is not None else [":", " ", "-", '"']
        elements = obj.findAll(tag, text=ele_text)
        if elements:
            value = elements[0].next_sibling
            for x in strip_list:
                value = value.strip(x)
        return value.strip()

    def run(self):
        try:
            self.load_data(
                reference_urls_path=self.config["reference_urls_path"],
                master_data_path=self.config["master_data_path"],
                success_urls_path=self.config["success_urls_path"],
                failed_urls_path=self.config["failed_urls_path"],
            )
        except AttributeError:
            print("No metadata found in bucket. Exiting...")
            sys.exit()

        try:
            for _, row in self.get_scraping_list_df().iterrows():
                self.extract_data(row[0], row[1])
        except Exception as e:
            print(f"Error occurred. Closing scraping process.\n{str(e)}")
        finally:
            self.save_data(
                master_data_path=self.config["master_data_path"],
                success_urls_path=self.config["success_urls_path"],
                failed_urls_path=self.config["failed_urls_path"],
            )
            sys.exit()


if __name__ == "__main__":
    config = load_config_yaml()["paths"]["PPPINDIA"]
    PPPINDIAScraper(config).run()
