import os
import json
from pathlib import Path
import yaml
import logging


def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent.parent.parent


def get_paths_yml():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "paths.yml"), "r") as yamlfile:
        data = yaml.load(yamlfile, Loader=yaml.FullLoader)
    return data


def get_path(key):
    return os.path.join(get_project_root(), get_paths_yml()["paths"]["texas_procurement"][key])


def get_county_location_data():
    logging.info("Geolocation data loaded")
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "county_location.json"), "r", encoding='utf-8') as jsonfile:
        data = json.load(jsonfile)
    return data
