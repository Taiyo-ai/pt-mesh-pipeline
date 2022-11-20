import geocoder

class data:
    def __init__(self):
        self.name = ""
        self.description = ""
        self.source=""
        self.status=""
        self.identified_status="" 
        self.project_or_tender=""
        self.budget= ""
        self.url= ""
        self.document_urls= ""
        self.sector= ""
        self.subsector= ""
        self.identified_sector= ""
        self.identified_subsector= ""
        self.identified_sector_subsector_tuple= ""
        self.entities= ""
        self.country_name= ""
        self.country_code= ""
        self.region_name= ""
        self.region_code= ""
        self.state= ""
        self.locality= ""
        self.neighbourhood= "" 
        self.location= ""
        self.map_coordinates=""
        self.timestamps= ""            
        self.timestamp_range= ""
        self.timestamp_range_2= ""



scraped_data=data
def geocode(a):
    g = geocoder.google(a)
    scraped_data.map_coordinates= a.latlng


def reverse_geocode(coords):
    g = geocoder.google(coords, method='reverse')
    n = geocoder.google("453 Booth Street, Ottawa ON")
    g.city
    g.state
    g.state_long
    g.country
    g.country_long

    #use for data
