import sys
import bs4
import requests

import pandas as pd

from ..utils import load_config_yaml
from ..utils.bucket import (
    connect_to_buffer_bucket,
    push_csv_to_buffer_bucket,
)


class PPPINDIAMetadataScraper:
    def __init__(self, config):
        self.project_count = 0
        self.config = config
        self.page_url_template = (
            "https://www.pppinindia.gov.in/infrastructureindia/web/guest/project-list"
            "?p_p_id=projectlist_WAR_Projectportlet"
            "&p_p_lifecycle=0"
            "&p_p_state=normal"
            "&p_p_mode=view"
            "&p_p_col_id=column-1"
            "&p_p_col_count=1"
            "&_projectlist_WAR_Projectportlet_jspPage=%2Fhtml%2Fprojectlist%2Fview.jsp"
            "&_projectlist_WAR_Projectportlet_searchName="
            "&_projectlist_WAR_Projectportlet_searchType=Government+Infrastructure+Projects+%28PPP%29"
            "&_projectlist_WAR_Projectportlet_id=1"
            "&_projectlist_WAR_Projectportlet_projectTypeeids="
            "&_projectlist_WAR_Projectportlet_authorityName="
            "&_projectlist_WAR_Projectportlet_isShowAllTerminatedProjects=false"
            "&_projectlist_WAR_Projectportlet_delta=20"
            "&_projectlist_WAR_Projectportlet_keywords="
            "&_projectlist_WAR_Projectportlet_advancedSearch=false"
            "&_projectlist_WAR_Projectportlet_andOperator=true"
            "&_projectlist_WAR_Projectportlet_orderByCol=modifiedDate"
            "&_projectlist_WAR_Projectportlet_orderByType=desc"
            "&_projectlist_WAR_Projectportlet_resetCur=false"
            "&_projectlist_WAR_Projectportlet_cur={}"
        )
        self.project_url_template = "https://www.pppinindia.gov.in/infrastructureindia/web/guest/project-list/{}"

    def get_project_ids(self):
        i = 0
        reached_last_pages = False
        project_ids = []
        while not reached_last_pages:
            print(f"Getting project_ids from page {i + 1}")
            page_url = self.page_url_template.format(i)
            html_data = requests.get(page_url).text
            temp_list = self.get_project_ids_from_page(html_data)
            i = i + 1
            if temp_list is None:
                reached_last_pages = True
                print("All pages scraped")
            else:
                project_ids.extend(temp_list)
        return project_ids

    def get_project_urls(self, project_ids):
        return [
            self.project_url_template.format(project_id.lower())
            for project_id in project_ids
        ]

    @staticmethod
    def get_project_ids_from_page(html_data):
        soup = bs4.BeautifulSoup(html_data, "lxml")
        tables = soup.findAll("tbody")
        if len(tables) == 0:
            return None
        else:
            rows = tables[0].findAll("tr")
        projects_ids = []
        if len(rows) == 0:
            return None
        else:
            for row in rows:
                project_id = row.findAll("td")[0].findAll("a")[0].contents[0]
                projects_ids.append(project_id)
        return projects_ids

    def run(self):
        try:
            project_ids = self.get_project_ids()
            project_urls = self.get_project_urls(project_ids)
            self.project_ids_urls_df = pd.DataFrame(
                list(zip(project_ids, project_urls)), columns=["project_id", "url"]
            )
        except Exception as e:
            print(
                f"Error occurred. Closing PPPINDIA Metadata scraping process.\n{str(e)}"
            )
        finally:
            self.bucket = connect_to_buffer_bucket()
            # push_csv_to_buffer_bucket(
            #     self.bucket,
            #     self.project_ids_urls_df,
            #     self.config["reference_urls_path"],
            # )
            self.project_ids_urls_df.to_csv(
                "ppp_india_metadata.csv", index=False, header=True
            )

            sys.exit()


if __name__ == "__main__":
    config = load_config_yaml()["paths"]["PPPINDIA"]
    PPPINDIAMetadataScraper(config).run()
