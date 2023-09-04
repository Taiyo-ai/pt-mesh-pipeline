from geopy.geocoders import Nominatim

def geocode_data(data):
    geolocator = Nominatim(user_agent="geoapiExercises")

    for entry in data:
        # Check if location information is available
        if "Location" in entry:
            location = entry["Location"]

            # Check if geo-spatial coordinates are missing
            if "Latitude" not in entry or "Longitude" not in entry:
                try:
                    # Use geocoding to obtain coordinates and location label
                    location_info = geolocator.geocode(location)

                    if location_info:
                        entry["Latitude"] = location_info.latitude
                        entry["Longitude"] = location_info.longitude
                        entry["Location Label"] = location_info.address
                except Exception as e:
                    print(f"Error geocoding for '{location}': {str(e)}")

    return data
