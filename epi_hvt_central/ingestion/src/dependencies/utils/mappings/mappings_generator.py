import yaml


primary_fields = set(
    [
        "aug_id",
        "original_id",
        "project_or_tender",
        "name",
        "description",
        "source",
        "status",
        "identified_status",
        "budget",
        "url",
        "sector",
        "subsector",
        "identified_sector",
        "identified_subsector",
        "identified_sector_subsector_tuple",
        "keywords",
        "entities",
        "country_name",
        "country_code",
        "region_name",
        "region_code",
        "state",
        "county",
        "city",
        "locality",
        "neighbourhood",
        "location",
        "map_coordinates",
        "timestamps",
        "timestamp_range",
    ]
)

with open("mappings.yaml") as f:
    data = yaml.load(f, Loader=yaml.SafeLoader)

mapping_keys = set(data["tenders_epihvtstate"]["mappings"]["properties"].keys())

print("Primary_keys: ", mapping_keys & primary_fields)
print("Secondary_keys: ", mapping_keys - primary_fields)

pri_mappings = {}
pri_mappings["settings"] = data["tenders_epihvtstate"]["settings"]
pri_mappings["mappings"] = {}
pri_mappings["mappings"]["properties"] = {}

sec_mappings = {}
sec_mappings["settings"] = data["tenders_epihvtstate"]["settings"]
sec_mappings["mappings"] = {}
sec_mappings["mappings"]["properties"] = {}

for key, value in data["tenders_epihvtstate"]["mappings"]["properties"].items():
    if key in mapping_keys & primary_fields:
        pri_mappings["mappings"]["properties"][key] = value
        if key in ["aug_id"]:
            sec_mappings["mappings"]["properties"][key] = value
    elif key in mapping_keys - primary_fields:
        sec_mappings["mappings"]["properties"][key] = value

with open("mappings_pri.yaml", "w") as f:
    yaml.dump(pri_mappings, f)

with open("mappings_sec.yaml", "w") as f:
    yaml.dump(sec_mappings, f)
