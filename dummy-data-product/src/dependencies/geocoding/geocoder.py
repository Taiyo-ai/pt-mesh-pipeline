

from geopy.geocoders import Nominatim
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.basemap import Basemap

def geocode_csv():
    geolocator = Nominatim(user_agent="tender")
    location = geolocator.geocode("India")
    if location is not None:
        latitude = location.latitude
        longitude = location.longitude
        print("Latitude:", latitude)
        print("Longitude:", longitude)
        mfig, ax = plt.subplots(figsize=(10, 6))
        m = Basemap(projection='mill', llcrnrlat=-90, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=180, resolution='c', ax=ax)
        m.drawcoastlines()
        m.drawcountries()
        m.drawstates()
        x, y = m(longitude, latitude)
        m.plot(x, y, 'ro', markersize=6)
        plt.title('Location on World Map')
        plt.show()



    else:
        print("Geocoding failed.")



