import folium
import pandas as pd

# Simulated Airbnb data with lat/long and some Airbnb info (normally you would load this from a real dataset)
data = {
    'address': ['Airbnb 1', 'Airbnb 2', 'Airbnb 3'],
    'latitude': [40.748817, 40.730610, 40.712776],
    'longitude': [-73.985428, -73.935242, -74.005974],
    'landmarks_nearby': [['Empire State Building', 'Chrysler Building'], ['Central Park'], ['Statue of Liberty', 'Wall Street']],
    'price': [150, 200, 250]
}

airbnb_data = pd.DataFrame(data)

# Create a map centered around NYC
nyc_map = folium.Map(location=[40.7128, -74.0060], zoom_start=12)

# Add Airbnb properties and nearby landmarks to the map
for index, row in airbnb_data.iterrows():
    # Add Airbnb property marker
    folium.Marker([row['latitude'], row['longitude']], popup=f"{row['address']} - Price: ${row['price']}", icon=folium.Icon(color='blue')).add_to(nyc_map)
    
    # Add landmarks as separate markers (offset lat/long slightly for visualization)
    if row['landmarks_nearby']:
        for landmark in row['landmarks_nearby']:
            # Offset the lat/long slightly for demo purposes
            folium.Marker([row['latitude'] + 0.001, row['longitude'] + 0.001], popup=landmark, icon=folium.Icon(color='green')).add_to(nyc_map)

# Save the map to an HTML file
nyc_map.save('nyc_airbnb_landmarks_map.html')

print("Map with Airbnb properties and landmarks saved as 'nyc_airbnb_landmarks_map.html'")
