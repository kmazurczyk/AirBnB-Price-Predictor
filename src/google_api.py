import os
import pandas as pd
import requests
import sys
from __init__ import get_base_path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(get_base_path() + '/airbnb.env')

# Access the API key from the environment variable
api_key = os.getenv('GOOGLE_API_KEY')
data_dir = get_base_path() + os.getenv('data_dir')

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

# Function to get address from latitude and longitude using Geocoding API
def get_address(lat, lng):
    url = f'https://maps.googleapis.com/maps/api/geocode/json?latlng={lat},{lng}&key={api_key}'
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
# if __name__ == "__main__":
#     # Example NYC address: Empire State Building
#     address = "350 5th Ave, New York, NY 10118"
    
#     # Get latitude and longitude for the address
#     lat, lng = get_lat_long(address)
#     print(f"Latitude: {lat}, Longitude: {lng}")

#     # Get address for latitude and longitude
#     address = get_address(lat,lng)
#     print(f"Address attributes: {addresses}")
    
#     # Get landmarks nearby the address
#     landmarks = get_landmarks_nearby(lat, lng)
#     print(f"Nearby Landmarks: {landmarks}")

# Airbnb Integration
def get_airbnb_listings(file_csv='airbnb_sample.csv',lat_long_only=False):

    try:
        file_path = data_dir + 'raw/' + file_csv
        df = pd.read_csv(file_path, index_col=0)
        df = df.sort_index()

        if lat_long_only == True:
            df = df.loc[:,['latitude','longitude']]
            return df
        else:
            return df

    except FileNotFoundError as f:
        print(f"Could not find {file_csv}. Expected path: {file_path}")

# Function to subset df as needed, to save Google API costs
def batch_listings(df,start,stop):

    batch_df = pd.DataFrame()
    start_index = 0
    end_index = 1000
    batch = 1000
    
    while end_index < size + 1:
        slice_df = df.iloc[start_index:end_index]
        batch_df = pd.concat([batch_df, slice_df], ignore_index=False)
        start_index = end_index
        end_index += batch    
    
    return batch_df

# Example integration between Airbnb API and Google APIs
if __name__ == "__main__":
    # Step 1: Fetch Airbnb property listings
    airbnb_listings = get_airbnb_listings(lat_long_only = True)

    # Optionally, batch to save cost
    airbnb_listings = batch_listings(airbnb_listings)

    # for property in airbnb_listings:
    #     address = property['address']  # Get address from the listing
        
    #     # Step 2: Get latitude and longitude for the property address
    #     lat, lng = get_lat_long(address)
        
    #     if lat is not None and lng is not None:
    #         print(f"Latitude: {lat}, Longitude: {lng}")
            
    #         # Step 3: Get landmarks near the property
    #         landmarks = get_landmarks_nearby(lat, lng)
    #         print(f"Nearby Landmarks for {address}: {landmarks}")
    #     else:
    #         print(f"Failed to get lat/lng for the address: {address}")
