import requests
import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# API keys from environment variables
geocoding_api_key = os.getenv("GOOGLE_GEOCODING_API_KEY")
places_api_key = os.getenv("GOOGLE_PLACES_API_KEY")

def geocode_address(row):
    """Convert address to latitude and longitude using Google Geocode API."""
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={row['address']}&key={geocoding_api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data.get('results'):
            row['lat'] = data['results'][0]['geometry']['location']['lat']
            row['lng'] = data['results'][0]['geometry']['location']['lng']
        else:
            row['lat'], row['lng'] = None, None
    else:
        print(f"Error in geocoding request: {response.status_code}")
    return row

def find_nearby_places(row, radius=500, place_type='point_of_interest'):
    """Get nearby places within a given radius using Google Places API."""
    if not row.get('lat') or not row.get('lng'):
        return row  # Skip if lat/lng is missing

    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={row['lat']},{row['lng']}&radius={radius}&type={place_type}&key={places_api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        row['num_landmarks'] = len(data['results'])
        row['landmark_names'] = [result['name'] for result in data['results']]
    else:
        row['num_landmarks'], row['landmark_names'] = 0, []
        print(f"Error in Places request: {response.status_code}")
    return row
