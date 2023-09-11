import traceback

from ..utils import load_config_yaml
from ..utils.bucket import (
    connect_to_buffer_bucket,
    push_csv_to_buffer_bucket,
    read_csv_from_buffer_bucket,
    read_excel_from_buffer_bucket,
    read_stata_from_buffer_bucket,
)


class BaseCleaner:
    """
    This is an abstract cleaner class.
    """

    def __init__(self):
        self.off2short_dict = {}
        self.country_name2code_dict = {}
        self.country_code2region_name_dict = {}
        self.region_name2code_dict = {}
        self.column_rename_dict = {}

        self.base_data = None
        self.raw_data = None

        self.bucket = connect_to_buffer_bucket()
        self.config = load_config_yaml()
        self.load_conversion_dictionaries(self.config["location_mapping_paths"])

    def load_data(self, paths):
        try:
            if paths["base_data_path"] != "None":
                # self.base_data = pd.read_csv(paths["base_data_path"])
                self.base_data = read_csv_from_buffer_bucket(
                    self.bucket, paths["base_data_path"]
                )
        except Exception as e:
            print(f"Error reading base data\n{e}\n")

        try:
            ext = paths["master_data_path"].split(".")[-1]
            if ext == "csv":
                # self.raw_data = pd.read_csv(paths["raw_data_path"])
                self.raw_data = read_csv_from_buffer_bucket(
                    self.bucket, paths["master_data_path"]
                )
            elif ext == "xlsx":
                # self.raw_data = pd.read_excel(paths["raw_data_path"])
                self.raw_data = read_excel_from_buffer_bucket(
                    self.bucket, paths["master_data_path"]
                )
            elif ext == "dta":
                # self.raw_data = pd.read_stata(paths["raw_data_path"])
                # self.column_rename_dict = pd.read_stata(paths["raw_data_path"],iterator=True).variable_labels()
                self.raw_data = read_stata_from_buffer_bucket(
                    self.bucket, paths["master_data_path"]
                )
                self.column_rename_dict = read_stata_from_buffer_bucket(
                    self.bucket, paths["master_data_path"], iterator=True
                ).variable_labels()
        except Exception as e:
            print(f"Error reading file from given path\n{e}\n")

    def load_conversion_dictionaries(self, paths):
        try:
            # off2short = pd.read_excel(paths["official_name2short_name"])
            off2short = read_excel_from_buffer_bucket(
                self.bucket, sheet_name="Sheet1", rel_path=paths["official_names"]
            )
            self.off2short_dict = dict(
                off2short[["Official Name", "Short Name"]].values.tolist()
            )
        except Exception as e:
            print("Error loading dict:", e, traceback.print_exc())

        try:
            # country_name2code = pd.read_excel(paths["country_region_incomegrp"],sheet_name='Country_income_grp')
            country_name2code = read_excel_from_buffer_bucket(
                self.bucket,
                sheet_name="Country_income_grp",
                rel_path=paths["region_and_income_group"],
            )
            self.country_name2code_dict = dict(
                country_name2code[["Country Name", "Code"]].values.tolist()
            )
        except Exception as e:
            print("Error loading dict:", e, traceback.print_exc())

        try:
            # country_code2region_name = pd.read_excel(paths["country_region_incomegrp"],
            #                                          sheet_name='Country_income_grp')
            country_code2region_name = read_excel_from_buffer_bucket(
                self.bucket,
                sheet_name="Country_income_grp",
                rel_path=paths["region_and_income_group"],
            )
            self.country_code2region_name_dict = dict(
                country_code2region_name[["Code", "Region"]].values.tolist()
            )
        except Exception as e:
            print("Error loading dict:", e, traceback.print_exc())

        try:
            # region_name2code = pd.read_excel(paths["country_region_incomegrp"],sheet_name='Region_codes')
            region_name2code = read_excel_from_buffer_bucket(
                self.bucket,
                sheet_name="Region_codes",
                rel_path=paths["region_and_income_group"],
            )
            self.region_name2code_dict = dict(
                region_name2code[["Region Name", "Region code"]].values.tolist()
            )
        except Exception as e:
            print("Error loading dict:", e, traceback.print_exc())

    def clean(self):
        """
        This is an unimplemented method where dataset can be cleaned using
        Pandas Library function
        """
        return None

    def run(self):
        """
        Unimplemented method - to execute the class
        """
        return None

    def save_data(self, cleaned_data, save_2_path):
        try:
            # if not os.path.exists(save_2_path.split('/')[0]):
            #     os.makedirs(save_2_path.split('/')[0])
            push_csv_to_buffer_bucket(self.bucket, cleaned_data, save_2_path)
            # cleaned_data.to_csv(save_2_path, header=True, index=False)
        except Exception as e:
            print(f"Error saving data\n{e}\n", traceback.print_exc())
