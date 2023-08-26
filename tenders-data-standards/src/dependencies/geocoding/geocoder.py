# import your dependencies here

import pandas as pd
from geopy.geocoders import Nominatim
import os

class Geocode:
    def __init__(self, **kwargs):
        self.csvfile = kwargs.get("csvfile")
        self.df = None
        self.output_file = 'geocoder_' + self.csvfile
        # Load the data
        # self.parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data'))
        # self.data_source_file_path = os.path.join(self.parent_directory, self.csvfile)

        self.df = pd.read_csv("../../data/" + self.csvfile , encoding='utf-16', delimiter='\t')

    def perfoem_geocoding(self):
        """Do extraction or processing of data here"""

        # Initialize geocoder
        geolocator = Nominatim(user_agent="geo_app")

        # Create empty lists to store location labels and coordinates
        location_labels = []
        coordinates = []

        # Iterate through the data and perform geocoding
        for index, row in self.df.iterrows():
            location = row['Location']  # Replace with the actual column name
            try:
                location_obj = geolocator.geocode(location , timeout=10)
                if location_obj:
                    location_labels.append(location)
                    coordinates.append((location_obj.latitude, location_obj.longitude))
                else:
                    location_labels.append("Not Found")
                    coordinates.append((None, None))
            except ValueError as e:
                location_labels.append("Error" + e)
                coordinates.append((None, None))

        # Add the new columns to the DataFrame
        self.df['Location_Label'] = location_labels
        self.df['Coordinates'] = coordinates

        # Save the updated DataFrame
    def save_data(self):
        # """Function to save data"""
        self.df.to_csv('../../data/' + self.output_file, encoding='utf-16' , sep='\t', index=False)

    def run(self):
        """Load data, do_something and finally save the data"""
        self.perfoem_geocoding()
        self.save_data()
