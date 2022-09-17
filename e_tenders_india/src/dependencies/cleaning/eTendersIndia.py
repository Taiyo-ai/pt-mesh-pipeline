from pandas.core.frame import DataFrame
from .BaseCleaner import BaseCleaner


class clean_eTendersIndia(BaseCleaner):
    def __init__(self, **kwargs):
        super().__init__()
        self.dataset_path = self.config["paths"]["ETENDERSINDIA"]
        self.load_data(self.dataset_path)

    def clean(self, df: DataFrame):
        try:
            df.dropna(subset=["tender_id"], inplace=True)
            df.drop_duplicates(subset="tender_id", keep="last", inplace=True)
            df.drop(
                list(df.filter(regex=r"^s.no_corrigendum_title_corrigendum_type_")),
                axis=1,
                inplace=True,
            )
            df.drop(
                list(df.filter(regex=r"^[0-9]")),
                axis=1,
                inplace=True,
            )

            df["data_source"] = "ETENDERSINDIA"
            df["country_code"] = "IND"
            df["country_name"] = "India"
            df["country"] = "India"

            df["map_coordinates"] = df["location"]

            df["aug_id"] = "ETENDERSINDIA_" + df["tender_id"]
            df["project_or_tender"] = "T"

            df["tender_fee_in_usd"] = df["tender_fee_in_₹"].apply(lambda x: x * 73.5621)
            df["emd_amount_in_usd"] = df["emd_amount_in_₹"].apply(lambda x: x * 73.5621)
            df["tender_value_in_usd"] = df["tender_value_in_₹"].apply(
                lambda x: x * 73.5621
            )

            return df

        except Exception as e:
            print(f"Error cleaning column:\n{e}\n")

    def run(self):
        try:
            self.cleaned_data = self.clean(self.raw_data)
        except Exception as e:
            print(f"Error cleaning data:{e}\n")
        finally:
            self.save_data(self.cleaned_data, self.dataset_path["cleaned_data_path"])


def main():
    clean_eTendersIndia().run()


if __name__ == "__main__":
    main()
