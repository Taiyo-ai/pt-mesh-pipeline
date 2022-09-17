import os
import sys
import yaml

from .bucket import (
    push_csv_to_buffer_bucket,
    connect_to_buffer_bucket,
    read_csv_from_buffer_bucket,
    read_excel_from_buffer_bucket,
    read_json_from_buffer_bucket,
)


def load_config_yaml(
    config_path=os.path.join(sys.path[0], "dependencies", "utils", "paths.yml")
):
    print()
    try:
        with open(config_path) as config_yaml:
            config = yaml.load(config_yaml, Loader=yaml.SafeLoader)
        return config
    except Exception as e:
        print("Error loading the projects data config file\n", e)
