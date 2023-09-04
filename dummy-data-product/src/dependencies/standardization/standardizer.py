def standardize_data(data):
    standardized_data = []

    for entry in data:
        standardized_entry = {}

        # Rename and standardize fields
        standardized_entry["tender_name"] = entry.get("Tender Name", "")
        standardized_entry["tender_details"] = entry.get("Tender Details", "")
        standardized_entry["location"] = entry.get("Location", "")
        
        # Standardize data types and consistency
        standardized_entry["latitude"] = float(entry.get("Latitude", 0.0))
        standardized_entry["longitude"] = float(entry.get("Longitude", 0.0))
        
        # Standardize sector and subsector fields
        sector = entry.get("Sector", "").lower().strip()
        subsector = entry.get("Subsector", "").lower().strip()
        standardized_entry["sector"] = sector
        standardized_entry["subsector"] = subsector
        
        # Map status and stage fields
        status = entry.get("Status", "").lower().strip()
        stage = entry.get("Stage", "").lower().strip()
        
        status_mapping = {
            "in progress": "ongoing",
            "completed": "finished",
            "cancelled": "canceled"
        }
        
        stage_mapping = {
            "preparation": "planning",
            "implementation": "in progress"
        }
        
        standardized_entry["status"] = status_mapping.get(status, status)
        standardized_entry["stage"] = stage_mapping.get(stage, stage)
        
        # Manipulate other fields as needed
        # Add additional transformations here
        
        standardized_data.append(standardized_entry)

    return standardized_data
