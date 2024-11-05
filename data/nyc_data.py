import pandas as pd
from math import radians, cos, sin, sqrt, atan2

# Load NYC Zip Codes and Boroughs Data
def load_nyc_data():
    nyc_zip_codes_url = 'https://data.cityofnewyork.us/resource/pri4-ifjk.csv'
    nyc_boroughs_url = 'https://data.cityofnewyork.us/resource/tqmj-j8zm.csv'

    nyc_zip_codes = pd.read_csv(nyc_zip_codes_url)
    nyc_boroughs = pd.read_csv(nyc_boroughs_url)
    return nyc_zip_codes, nyc_boroughs

# Feature Engineering for distance calculations (if needed)
def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return 6371 * c  # Returns distance in kilometers
