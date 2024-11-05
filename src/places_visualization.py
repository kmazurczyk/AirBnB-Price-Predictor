from __init__ import get_base_path
from dotenv import load_dotenv
from sample_airbnb import sample_df
import folium
import os
import pandas as pd
import sys

# environment
load_dotenv(get_base_path() + '/airbnb.env')
data_dir = get_base_path() + os.getenv('data_dir')

# Load Airbnb data
path = data_dir + 'processed/' + 'airbnb_sample' + '.csv'
airbnb_data = pd.read_csv(path)
airbnb_data = sample_df(df=airbnb_data, n=1000, weights=None)
print(f"Loaded Airbnb Data - {airbnb_data.shape[0]} rows, {airbnb_data.shape[1]} columns")

# Load Landmarks data
path = data_dir + 'processed/' + 'NYC_famous_landmarks_list' + '.csv'
landmarks_data = pd.read_csv(path)
print(f"Loaded {landmarks_data.shape[0]} landmarks")

# Create a map centered around NYC
nyc_map = folium.Map(location=[40.7128, -74.0060], zoom_start=12)

# Add Airbnb properties and nearby landmarks to the map
for index, row in airbnb_data.iterrows():
    # Add Airbnb property marker
    folium.Marker(
        [row['latitude'], row['longitude']],
        popup=f"AirBNB - Price: ${row['price']}",
        icon=folium.Icon(color='blue')
    ).add_to(nyc_map)
    
# Add landmarks as separate markers
for index, row in landmarks_data.iterrows():
    # Add Airbnb property marker
    folium.Marker(
        [row['latitude'], row['longitude']],
        popup=row['landmark'],  # Display landmark name
        icon=folium.Icon(color='green')
        ).add_to(nyc_map)
                
# Save the map to an HTML file
nyc_map.save('nyc_airbnb_landmarks_map.html')

print("Map with Airbnb properties and landmarks saved as 'nyc_airbnb_landmarks_map.html'")

