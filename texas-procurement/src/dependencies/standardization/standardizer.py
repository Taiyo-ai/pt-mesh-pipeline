import pandas as pd
import logging
import pytz
import spacy
from dependencies.utils import get_path


def get_sector(x):
    x = x.lower()
    if "road" in x or "rail" in x or "highway" in x or "transport" in x or "airport" in x or "transit" in x or "port" in x or "bridge" in x:
        return "Transport"
    return "Maintenance/Infrastructure"


def get_subsector(x):
    x = x.lower()
    if "road" in x or "highway" in x:
        return "Roadways"
    if "bridge" in x:
        return "Roads - Bridges and Tunnels"
    if "rail" in x:
        return "Railways"
    if "airport" in x:
        return "Aviation/Airports"
    if "transport" in x:
        return "Urban Public Transport"
    if "transit" in x:
        return "Public Transit"
    if "port" in x:
        return "Ports/Harbour/Shipyard"
    return "Repair and Upgrade"


class TexasStandardizer:

    def __init__(self) -> None:
        self.df = None

    def load_data(self):
        self.df = pd.read_csv(get_path("geocoded_data_path"), keep_default_na=False, index_col=0)

    def process(self):
        c_list_new = []
        for c in list(self.df.columns):
            c = c.strip().replace("  ", " ").replace(" ", "_").lower()
            c_list_new.append(c)
        self.df.columns = c_list_new
        self.df.rename(columns={
            "project_id": "original_id",
            "construction_cost/estimate": "budget",
            "category1_description": "name"
        }, inplace=True)
        self.df["aug_id"] = self.df["original_id"].apply(lambda x: f"self.dfdot_{x}")
        # self.df["name"] = self.df.apply(lambda row: f"{row.description} at highway {row.highway} from {row.from_limit} to {row.to_limit}, {row.status} by {row.construction_company_contact}", axis=1)
        self.df["source"] = "Texas Department of Transportation Official Website"
        self.df["url"] = "https://apps3.self.dfdot.gov/apps-cq/project_tracker/"
        self.df["document_urls"] = "ftp://ftp.dot.state.self.df.us/pub/self.dfdot-info/tpp/project-tracker/Project_Tracker.xls"
        self.df["state"] = "Texas"

        self.df["last_update_date"] = self.df["last_update_date"].apply(lambda x: pd.to_datetime(x).tz_localize("US/Central").tz_convert(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S%z") if x != "TBD" else "")
        self.df["bid_received_date"] = self.df["bid_received_date"].apply(lambda x: pd.to_datetime(x).tz_localize(tz="US/Central").tz_convert(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S%z") if x != "TBD" else "")
        self.df["design_30%_complete_target"] = self.df["design_30%_complete_target"].apply(lambda x: pd.to_datetime(x).tz_localize(tz="US/Central").tz_convert(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S%z") if x != "TBD" else "")
        self.df["design_30%_complete_actual"] = self.df["design_30%_complete_actual"].apply(lambda x: pd.to_datetime(x).tz_localize(tz="US/Central").tz_convert(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S%z") if x != "TBD" else "")
        self.df["design_60%_complete_target"] = self.df["design_60%_complete_target"].apply(lambda x: pd.to_datetime(x).tz_localize(tz="US/Central").tz_convert(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S%z") if x != "TBD" else "")
        self.df["design_60%_complete_actual"] = self.df["design_60%_complete_actual"].apply(lambda x: pd.to_datetime(x).tz_localize(tz="US/Central").tz_convert(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S%z") if x != "TBD" else "")
        self.df["design_100%_complete_target"] = self.df["design_100%_complete_target"].apply(lambda x: pd.to_datetime(x).tz_localize(tz="US/Central").tz_convert(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S%z") if x != "TBD" else "")
        self.df["design_100%_complete_actual"] = self.df["design_100%_complete_actual"].apply(lambda x: pd.to_datetime(x).tz_localize(tz="US/Central").tz_convert(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S%z") if x != "TBD" else "")
        self.df["notice_to_proceed_date"] = self.df["notice_to_proceed_date"].apply(lambda x: pd.to_datetime(x).tz_localize(tz="US/Central").tz_convert(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S%z") if x != "TBD" else "")
        self.df["work_begin_date"] = self.df["work_begin_date"].apply(lambda x: pd.to_datetime(x).tz_localize(tz="US/Central").tz_convert(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S%z") if x != "TBD" else "")
        self.df["start_design_target"] = self.df["start_design_target"].apply(lambda x: pd.to_datetime(x).tz_localize(tz="US/Central").tz_convert(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S%z") if x != "TBD" else "")
        self.df["start_design_actual"] = self.df["start_design_actual"].apply(lambda x: pd.to_datetime(x).tz_localize(tz="US/Central").tz_convert(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S%z") if x != "TBD" else "")
        self.df["received_environmental_clearance_target"] = self.df["received_environmental_clearance_target"].apply(lambda x: pd.to_datetime(x).tz_localize(tz="US/Central").tz_convert(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S%z") if x != "TBD" else "")
        self.df["received_environmental_clearance_actual"] = self.df["received_environmental_clearance_actual"].apply(lambda x: pd.to_datetime(x).tz_localize(tz="US/Central").tz_convert(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S%z") if x != "TBD" else "")
        self.df["utility_coordination_target"] = self.df["utility_coordination_target"].apply(lambda x: pd.to_datetime(x).tz_localize(tz="US/Central").tz_convert(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S%z") if x != "TBD" else "")
        self.df["utility_coordination_actual"] = self.df["utility_coordination_actual"].apply(lambda x: pd.to_datetime(x).tz_localize(tz="US/Central").tz_convert(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S%z") if x != "TBD" else "")
        self.df["right_of_way_coordination_target"] = self.df["right_of_way_coordination_target"].apply(lambda x: pd.to_datetime(x).tz_localize(tz="US/Central").tz_convert(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S%z") if x != "TBD" else "")
        self.df["right_of_way_coordination_actual"] = self.df["right_of_way_coordination_actual"].apply(lambda x: pd.to_datetime(x).tz_localize(tz="US/Central").tz_convert(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S%z") if x != "TBD" else "")
        self.df["project_ready_to_bid_target"] = self.df["project_ready_to_bid_target"].apply(lambda x: pd.to_datetime(x).tz_localize(tz="US/Central").tz_convert(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S%z") if x != "TBD" else "")
        self.df["project_ready_to_bid_actual"] = self.df["project_ready_to_bid_actual"].apply(lambda x: pd.to_datetime(x).tz_localize(tz="US/Central").tz_convert(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S%z") if x != "TBD" else "")
        self.df["contact_last_update"] = self.df["contact_last_update"].apply(lambda x: pd.to_datetime(x, errors="ignore").tz_localize(tz="US/Central").tz_convert(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S%z") if x != "" else "")
        self.df["construction_last_update"] = self.df["construction_last_update"].apply(lambda x: pd.to_datetime(x).tz_localize(tz="US/Central").tz_convert(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S%z") if x != "" else "")
        self.df["finance_last_update"] = self.df["finance_last_update"].apply(lambda x: pd.to_datetime(x).tz_localize(tz="US/Central").tz_convert(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S%z") if x != "" else "")
        self.df["funding_last_update"] = self.df["funding_last_update"].apply(lambda x: pd.to_datetime(x).tz_localize(tz="US/Central").tz_convert(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S%z") if x != "" else "")
        self.df["milestone_last_update"] = self.df["milestone_last_update"].apply(lambda x: pd.to_datetime(x).tz_localize(tz="US/Central").tz_convert(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S%z") if x != "" else "")
        self.df["project_last_update"] = self.df["project_last_update"].apply(lambda x: pd.to_datetime(x).tz_localize(tz="US/Central").tz_convert(pytz.utc).strftime("%Y-%m-%dT%H:%M:%S%z") if x != "" else "")

        self.df["budget"] = self.df["budget"].apply(lambda x: float(x) if x != "" else "")
        self.df["percentage_of_time_used"] = self.df["percentage_of_time_used"].apply(lambda x: float(x) if x != "" else "")
        self.df["percentage_of_budget_used"] = self.df["percentage_of_budget_used"].apply(lambda x: float(x) if x != "" else "")
        self.df["project_engineering_cost_to_date"] = self.df["project_engineering_cost_to_date"].apply(lambda x: float(x) if x != "" else "")
        self.df["construction_cost_to_date"] = self.df["construction_cost_to_date"].apply(lambda x: float(x) if x != "" else "")
        self.df["construction_engineering_cost_to_date"] = self.df["construction_engineering_cost_to_date"].apply(lambda x: float(x) if x != "" else "")
        self.df["total_cost_to_date"] = self.df["total_cost_to_date"].apply(lambda x: float(x) if x != "" else "")
        self.df["category1_amount"] = self.df["category1_amount"].apply(lambda x: float(x) if x != "" else "")
        self.df["category2_amount"] = self.df["category2_amount"].apply(lambda x: float(x) if x != "" else "")
        self.df["category3_amount"] = self.df["category3_amount"].apply(lambda x: float(x) if x != "" else "")
        self.df["category4_amount"] = self.df["category4_amount"].apply(lambda x: float(x) if x != "" else "")
        self.df["category5_amount"] = self.df["category5_amount"].apply(lambda x: float(x) if x != "" else "")
        self.df["category6_amount"] = self.df["category6_amount"].apply(lambda x: float(x) if x != "" else "")
        self.df["category7_amount"] = self.df["category7_amount"].apply(lambda x: float(x) if x != "" else "")
        self.df["category8_amount"] = self.df["category8_amount"].apply(lambda x: float(x) if x != "" else "")
        self.df["category9_amount"] = self.df["category9_amount"].apply(lambda x: float(x) if x != "" else "")
        self.df["category10_amount"] = self.df["category10_amount"].apply(lambda x: float(x) if x != "" else "")

        self.df["project_or_tender"] = self.df["construction_company_contact"].apply(lambda x: "T" if x == "" else "P")
        self.df["identified_status"] = self.df["construction_company_contact"].apply(lambda x: "Active" if x == "" else "Closed")
        self.df["sector"] = self.df["description"].apply(lambda x: get_sector(x))
        self.df["subsector"] = self.df["description"].apply(lambda x: get_subsector(x))
        self.df["identified_sector_subsector_tuple"] = self.df.apply(lambda row: (row.sector, row.subsector), axis=1)
        self.df["text"] = self.df[["description", "status", "name"]].agg(", ".join, axis=1)
        nlp = spacy.load("en_core_web_trf")
        self.df["keyword"] = self.df["text"].apply(lambda x: nlp(x).ents)

    def save_data(self):
        self.df.to_csv(get_path("standardized_data_path"))

    def run(self):
        logging.info("Standardizing Started")
        self.load_data()
        self.process()
        self.save_data()
        logging.info("Standardizing Done")


if __name__ == "__main__":
    # Example configuration dictionary
    config = {
        # class specific configuration
        "webdriver_path": "path_to_webdriver",
        "PROCESSES": 15,

        # path configurations
        "path_config": {
            "meta_data_path": "rel_path",
            "raw_data_path": "rel_path",
            "cleaned_data_path": "rel_path",
            "geocoded_data_path": "rel_path",
            "standardized_data_path": "rel_path",
        }
    }
    obj = TexasStandardizer(config=config)
    obj.run()
