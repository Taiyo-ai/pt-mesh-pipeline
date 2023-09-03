# dependencies/geocoding/step_4.py
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import os

class step_4:
    def __init__(self, config):
        self.config = config

    def run(self):
        # Load your data (assuming it's in a DataFrame)
        data = self.load_data()

        # Perform geocoding and reverse geocoding operations
        geocoded_data = self.geocode_locations(data)
        geocoded_data = self.reverse_geocode_missing(data, geocoded_data)

        # Save or use the geocoded data as needed
        self.save_geocoded_data(geocoded_data)

    def load_data(self):
        # Load your data here (e.g., from a CSV file or a database)
        data = pd.read_csv(self.config['data_file'])
        return data

    def geocode_locations(self, data):
        # Initialize a geocoder
        geolocator = Nominatim(user_agent=self.config['geocoder_user_agent'])

        # Geocode existing location information
        data['location_coordinates'] = data['location_label'].apply(self.geocode_location, geolocator=geolocator)
        return data

    def geocode_location(self, location_label, geolocator):
        try:
            location = geolocator.geocode(location_label)
            if location:
                return (location.latitude, location.longitude)
        except GeocoderTimedOut:
            pass
        return None

    def reverse_geocode_missing(self, data, geocoded_data):
        # Reverse geocode missing locations
        missing_data = data[data['location_coordinates'].isnull()]

        for index, row in missing_data.iterrows():
            if pd.notna(row['latitude']) and pd.notna(row['longitude']):
                location = self.reverse_geocode_coordinates(row['latitude'], row['longitude'])
                if location:
                    geocoded_data.at[index, 'location_coordinates'] = (row['latitude'], row['longitude'])
                    geocoded_data.at[index, 'location_label'] = location

        return geocoded_data

    def reverse_geocode_coordinates(self, latitude, longitude):
        # Implement reverse geocoding logic here
        # Use a geocoding service or library that supports reverse geocoding
        # Return the location label based on coordinates
        return None

def save_geocoded_data(self, geocoded_data):
    # Define the data folder
    data_folder = 'data'

    # Create the data folder if it doesn't exist
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    # Specify the CSV file name (without the folder name)
    geocoded_data_csv = self.config['geocoded_data_csv']

    # Construct the full file path with the data folder
    csv_file_path = os.path.join(data_folder, geocoded_data_csv)

    # Save the geocoded data to a CSV file within the 'data' folder
    geocoded_data.to_csv(csv_file_path, index=False)
