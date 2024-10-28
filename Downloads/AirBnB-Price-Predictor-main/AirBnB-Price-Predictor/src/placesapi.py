import folium
import pandas as pd
from data.google_api import find_nearby_places  # Ensure this is where `find_nearby_places` is implemented

# Load Airbnb data
airbnb_data = pd.read_csv('data/airbnb_data.csv')  # Use your actual Airbnb dataset with lat/long info

# Add nearby landmarks using Google Places API
def add_nearby_landmarks(data):
    data['landmarks_nearby'] = data.apply(
        lambda row: find_nearby_places(row['latitude'], row['longitude']),
        axis=1
    )
    return data

# Add the landmarks to the Airbnb data
airbnb_data = add_nearby_landmarks(airbnb_data)

# Create a map centered around NYC
nyc_map = folium.Map(location=[40.7128, -74.0060], zoom_start=12)

# Add Airbnb properties and nearby landmarks to the map
for index, row in airbnb_data.iterrows():
    # Add Airbnb property marker
    folium.Marker(
        [row['latitude'], row['longitude']],
        popup=f"{row['address']} - Price: ${row['price']}",
        icon=folium.Icon(color='blue')
    ).add_to(nyc_map)
    
    # Add landmarks as separate markers
    if row['landmarks_nearby']:
        for landmark in row['landmarks_nearby']:
            # Offset for visualization, adjust as needed
            folium.Marker(
                [row['latitude'] + 0.001, row['longitude'] + 0.001],
                popup=landmark['name'],  # Display landmark name
                icon=folium.Icon(color='green')
            ).add_to(nyc_map)

# Save the map to an HTML file
nyc_map.save('nyc_airbnb_landmarks_map.html')

print("Map with Airbnb properties and landmarks saved as 'nyc_airbnb_landmarks_map.html'")

