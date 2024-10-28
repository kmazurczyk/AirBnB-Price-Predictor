import folium
import pandas as pd
from src.google_api import find_nearby_places  # Adjust this if needed for path

# Load Airbnb data with lat/long and price information
airbnb_data = pd.read_csv('data/airbnb_listings_cleaned.csv')  # Ensure this file is in the correct location

# Function to add landmarks to Airbnb data
def add_landmarks_to_data(data):
    data['landmarks_nearby'] = data.apply(
        lambda row: find_nearby_places(row['latitude'], row['longitude']), axis=1
    )
    return data

# Add landmarks using Google Places API
airbnb_data = add_landmarks_to_data(airbnb_data)

# Create a map centered around NYC
nyc_map = folium.Map(location=[40.7128, -74.0060], zoom_start=12)

# Add Airbnb properties and their nearby landmarks to the map
for index, row in airbnb_data.iterrows():
    # Add Airbnb property marker
    folium.Marker(
        [row['latitude'], row['longitude']],
        popup=f"{row['address']} - Price: ${row['price']}",
        icon=folium.Icon(color='blue')
    ).add_to(nyc_map)
    
    # Add each landmark as a separate marker
    if row['landmarks_nearby']:
        for landmark in row['landmarks_nearby']:
            folium.Marker(
                [landmark['lat'], landmark['lng']],
                popup=landmark['name'],  # Use the landmark's name
                icon=folium.Icon(color='green')
            ).add_to(nyc_map)

# Save the map to an HTML file for visualization
nyc_map.save('output/nyc_airbnb_landmarks_map.html')
print("Map with Airbnb properties and landmarks saved as 'output/nyc_airbnb_landmarks_map.html'")
