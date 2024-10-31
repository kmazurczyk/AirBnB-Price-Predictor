import requests
import os
import time

API_KEY = os.getenv("GOOGLE_API_KEY")

def geocode_address(row):
    """Convert address to latitude and longitude using Google Geocode API."""
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={row['address']}&key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            row['lat'] = data['results'][0]['geometry']['location']['lat']
            row['lng'] = data['results'][0]['geometry']['location']['lng']
    return row

# Function to get address from latitude and longitude using Geocoding API
def get_address(lat, lng, api_key, result_type='street_address'):
    location_type='ROOFTOP'
    url = f'https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&location_type={location_type}&result_type={result_type}&key={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'results' in data and len(data['results']) > 0:
            addresses = data['results'][0]
            return addresses
        else:
            return None
    else:
        raise Exception(f"Error: {response.status_code, response.headers, response.text}")

def geocode_lat_long(address, api_key):
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'results' in data and len(data['results']) > 0:
            location = data['results'][0]['geometry']['location']
            return location['lat'], location['lng']
        else:
            return None
    else:
        raise Exception(f"Error: {response.status_code}")

def find_nearby_places(lat, lng, radius=500, place_type='landmark', retries=3):
    """Get nearby landmarks within a given radius, with retry mechanism for connection stability."""
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={radius}&type={place_type}&key={API_KEY}"
    
    for attempt in range(retries):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raises HTTPError for bad responses
            data = response.json()
            
            # Extract relevant information for each landmark
            landmarks = [{'name': result.get('name'), 
                          'lat': result['geometry']['location']['lat'],
                          'lng': result['geometry']['location']['lng']} 
                         for result in data.get('results', [])]
            
            return landmarks
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(2)  # Wait before retrying
    
    print("All retries failed.")
    return []  # Return an empty list if all attempts fail
