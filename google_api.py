import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the API key from the environment variable
api_key = os.getenv('GOOGLE_API_KEY')

# Function to get latitude and longitude from an address using Geocoding API
def get_lat_long(address):
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

import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the API key from the environment variable
api_key = os.getenv('GOOGLE_API_KEY')

# Function to get latitude and longitude from an address using Geocoding API
def get_lat_long(address):
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

# Function to get nearby landmarks using Places API
def get_landmarks_nearby(lat, lng, radius=500):
    url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius={radius}&key={api_key}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        landmarks = [(place['name'], place['vicinity']) for place in data['results']]
        return landmarks
    else:
        raise Exception(f"Error: {response.status_code}")

# Example usage
if __name__ == "__main__":
    # Example NYC address: Empire State Building
    address = "350 5th Ave, New York, NY 10118"
    
    # Get latitude and longitude for the address
    lat, lng = get_lat_long(address)
    print(f"Latitude: {lat}, Longitude: {lng}")
    
    # Get landmarks nearby the address
    landmarks = get_landmarks_nearby(lat, lng)
    print(f"Nearby Landmarks: {landmarks}")


# Airbnb API Integration
def get_airbnb_listings():
    # This is a placeholder function for calling the Airbnb API
    # You will need to replace this with actual Airbnb API code
    return [
        {"address": "350 5th Ave, New York, NY 10118"},  # Example: Empire State Building
        {"address": "1 World Trade Center, New York, NY 10007"}  # Example: One World Trade Center
    ]

# Example integration between Airbnb API and Google APIs
if __name__ == "__main__":
    # Step 1: Fetch Airbnb property listings from Airbnb API
    airbnb_listings = get_airbnb_listings()

    for property in airbnb_listings:
        address = property['address']  # Get address from the listing
        
        # Step 2: Get latitude and longitude for the property address
        lat, lng = get_lat_long(address)
        
        if lat is not None and lng is not None:
            print(f"Latitude: {lat}, Longitude: {lng}")
            
            # Step 3: Get landmarks near the property
            landmarks = get_landmarks_nearby(lat, lng)
            print(f"Nearby Landmarks for {address}: {landmarks}")
        else:
            print(f"Failed to get lat/lng for the address: {address}")
