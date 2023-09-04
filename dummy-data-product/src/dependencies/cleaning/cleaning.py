def clean_data(raw_data):
    cleaned_data = []
    seen_names = set()  # To keep track of duplicate entries

    for entry in raw_data:
        # Check if any required fields are missing, skip the entry if any are missing
        if "Tender Name" not in entry or "Tender Details" not in entry:
            continue

        # Conversion of amounts to USD (if applicable)
        # Replace this with your logic to convert amounts

        # Convert country codes to ISO 3166-1 alpha3 format (if applicable)
        # Replace this with your logic to convert country codes

        # Identify region name and region code using the country code (if applicable)
        # Replace this with your logic to identify region details

        name = entry["Tender Name"]

        # Treatment of duplicate entries
        if name not in seen_names:
            cleaned_data.append(entry)
            seen_names.add(name)

    return cleaned_data
