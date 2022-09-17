import sys
import bs4
import requests
import traceback

import pandas as pd

import multiprocessing

from ..scraping import BaseScraper
from ..utils import load_config_yaml


class ETendersIndiaScraper(BaseScraper):
    def __init__(self, config):
        self.config = config
        self.raw_data = pd.DataFrame()

        super().__init__(None, None)

    @staticmethod
    def extract_data(row):
        url, tender_id = row

        result = {"page_data": None, "success": False}

        def extract_tables(tables):
            merged_df: pd.DataFrame = None
            try:
                # Table 1
                df = pd.read_html(str(tables[0]))[0]
                df1 = df.drop(columns=[2, 3, 4, 5])
                df2 = (
                    df.drop(columns=[0, 1, 4, 5]).iloc[3:].rename(columns={2: 0, 3: 1})
                )
                merged_df = df1.append(df2)

                # Table 2
                df = pd.read_html(
                    str(tables[1].find("table").find("table").find("table"))
                )[0]
                df = df.drop(0, axis=1)
                df[0] = df[1][0]
                df[1][0] = (
                    df.iloc[1:].groupby(0)[1].apply(", ".join).reset_index(drop=True)[0]
                )
                df = df.iloc[[0]]
                merged_df = merged_df.append(df)

                # Table 3
                df = pd.read_html(str(tables[2].find("table").find("table")))[0]
                df = df.drop(0, axis=1)
                df.columns = df.iloc[0]
                df = df.drop(0, axis=0)
                cover_details = [
                    {
                        "cover_type": row["Cover Type"],
                        "description": row["Description"],
                        "document_type": row["Document Type"],
                    }
                    for _, row in df.iterrows()
                ]
                df1 = pd.DataFrame({0: "cover_details", 1: [cover_details]})
                merged_df = merged_df.append(df1)

                # Table 4
                df = pd.read_html(str(tables[3]))[0]
                df1 = df.drop(columns=[2, 3])
                df2 = df.drop(columns=[0, 1]).iloc[[1]].rename(columns={2: 0, 3: 1})
                merged_df = merged_df.append([df1, df2])

                # Table 5
                df = pd.read_html(str(tables[4]))[0]
                df1 = df.drop(columns=[2, 3])
                df2 = df.drop(columns=[0, 1]).rename(columns={2: 0, 3: 1})
                merged_df = merged_df.append([df1, df2])

                # Table 6
                df = pd.read_html(str(tables[5]))[0]
                df1 = df.drop(columns=[2, 3, 4, 5])
                df2 = (
                    df.drop(columns=[0, 1, 2, 3])
                    .iloc[4:-1]
                    .rename(columns={4: 0, 5: 1})
                )
                df3 = (
                    df.drop(columns=[0, 1, 4, 5]).iloc[4:].rename(columns={2: 0, 3: 1})
                )
                merged_df = merged_df.append([df1, df2, df3])

                # Table 7
                df = pd.read_html(str(tables[6]))[0]
                df1 = df.drop(columns=[2, 3])
                df2 = df.drop(columns=[0, 1]).rename(columns={2: 0, 3: 1})
                merged_df = merged_df.append([df1, df2])

                # Table 8 TODO: Include after sorting out Captcha issue
                # df1 = pd.read_html(str(tables[7].find_all("table")[3]))[0]
                # df2 = pd.read_html(str(tables[7].find("table")))[0]
                # merged_df = merged_df.append([df1, df2])

                # Table 9
                df = pd.read_html(str(tables[8]))[0]
                merged_df = merged_df.append(df)

                # Transform
                merged_df = merged_df.reset_index(drop=True).transpose()
                merged_df.columns = merged_df.iloc[0]
                merged_df.drop(0, inplace=True)
                merged_df.columns = [
                    i.replace(" ", "_").lower() for i in merged_df.columns.tolist()
                ]
            except Exception as e:
                print(traceback(e))
            finally:
                return merged_df

        retry = 5
        while retry > 0:
            try:
                session = requests.Session()

                soup = bs4.BeautifulSoup(session.get(url).text, "html.parser")
                tables = soup.find_all("table", class_="tablebg")

                page_data = extract_tables(tables=tables)
                page_data["url"] = url

                page_data = page_data.to_dict(orient="records")

                # consolidating data
                print(f"Scraped url: {url}")
                result = {"page_data": page_data, "success": True}
                break
            except Exception as e:
                print(f"Error occurred for url: {url} - {str(e)}")
                retry -= 1
        return result

    def run(self):
        try:
            self.load_data(
                reference_urls_path=self.config["reference_urls_path"],
                master_data_path=self.config["master_data_path"],
                success_urls_path=self.config["successful_urls_path"],
                failed_urls_path=self.config["failed_urls_path"],
            )
        except AttributeError:
            print("No metadata found in bucket. Exiting...")
            sys.exit()

        try:
            pool = multiprocessing.Pool(processes=multiprocessing.cpu_count() - 1)
            final_result = pool.map(
                self.extract_data, self.scraping_list_df.values.tolist()
            )
            # print("Overriding defaults, rescraping entire data...")
            # final_result = pool.map(
            #     self.extract_data, self.project_ids_urls_df.values.tolist()
            # )
            for result in final_result:
                if result["success"]:
                    self.add_to_collected_data(result["page_data"][0])
                    try:
                        self.add_url_to_success_list(
                            result["page_data"][0]["tender_id"],
                            result["page_data"][0]["url"],
                        )
                    except Exception as e:
                        self.add_url_to_success_list(
                            "NA",
                            result["page_data"][0]["url"],
                        )
                else:
                    self.add_url_to_failed_list(
                        "NA",
                        result["page_data"][0]["url"],
                    )

            pool.close()  # no more tasks
            pool.join()  # wrap up current tasks

        except Exception as e:
            print(f"Error occurred. Closing scraping process.\n{traceback(e)}")
        finally:
            # pd.DataFrame(self.collected_data).to_csv(
            #     "etendersindia_data.csv", index=False, header=True
            # )
            self.save_data(
                master_data_path=self.config["master_data_path"],
                success_urls_path=self.config["successful_urls_path"],
                failed_urls_path=self.config["failed_urls_path"],
                drop_dups_cols="url",
            )
            sys.exit()


if __name__ == "__main__":
    config = load_config_yaml()["paths"]["ETENDERSINDIA"]
    ETendersIndiaScraper(config).run()
