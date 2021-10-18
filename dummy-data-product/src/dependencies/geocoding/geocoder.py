
import requests
import time
from geopy.geocoders import Nominatim






class Geocode :
    
    
    def __init__(self,country_name,city_name):
        self.country_name=country_name
        self.city_name=city_name
    
    def geolocate(self):
        city_name=self.city_name
        country_name=self.country_name
        geolocator = Nominatim(user_agent="tutorial")
        try:
             # Geolocate the center of the country
            time.sleep(1)
            location= city_name + ' ' + country_name
            data = geolocator.geocode(location).raw
            latitude = data["lat"]
            longitude = data["lon"]
             # And return latitude and longitude
            return (latitude, longitude)
        except:
             # Return missing value
    # =============================================================================
             location= city_name + ' ' + country_name
             api_key = 'm8gyTg3agkqa5Vr-2a58bw4X9VyuvZDTGq1L3KZpO28' # Acquire from developer.here.com
             URL = "https://geocode.search.hereapi.com/v1/geocode?apikey={0}&q={1}".format(api_key,location)
    # =============================================================================
    
             r = requests.get(url = URL) 
             data = r.json()
             latitude = data['items'][0]['position']['lat']
             longitude = data['items'][0]['position']['lng']
    # =============================================================================
             return ( latitude , longitude )
         #return (np.nan,np.nan)

        



