import json

from geopy.geocoders import Nominatim
import os


class GeoCoder():

    def __init__(self, address_details):
        self.address_details = address_details
        if not os.path.isfile('Coordinates.json'):
            self.coordinate_dictionary = {}
        else:
            with open('Coordinates.json', 'r') as file_read:
                self.coordinate_dictionary = json.loads(file_read.read())
    def geo_coder(self):

        """First preference for Gecode is googlemaps api for more accuracy.
        But I have used geopy because it has free version"""

        locator = Nominatim(user_agent='my_geocode')
        try:
            if self.address_details in self.coordinate_dictionary:
                return self.coordinate_dictionary[self.address_details]
            return 'Coordinates delay' # Commenting this out will get you coordinates But will take time

            address_obj = locator.geocode(self.address_details)
            address_value = self.address_details
            while address_obj is None:
                # print(address_value)
                address_value = address_value.split(',', 1)[-1].strip()
                address_obj = locator.geocode(address_value)
        except:
            address_obj = None

        if address_obj:
            self.coordinate_dictionary[self.address_details] = fr'{address_obj.latitude}, {address_obj.longitude}'
            with open('Coordinates.json', 'w') as file_write:
                file_write.write(json.dumps(self.coordinate_dictionary))
        return fr'{address_obj.latitude}, {address_obj.longitude}'\
            if address_obj else 'Coordinates not available'





