# src/visualization.py

import folium
import pandas as pd
import matplotlib.pyplot as plt
from src.google_api import find_nearby_places  # Adjust this if needed for path

# Load Airbnb data with lat/long and price information
airbnb_data = pd.read_csv('data/airbnb_listings_cleaned.csv')  # Ensure this file is in the correct location

# Function to add landmarks to Airbnb data
def add_landmarks_to_data(data):
    data['landmarks_nearby'] = data.apply(
        lambda row: find_nearby_places(row['latitude'], row['longitude']), axis=1
    )
    return data

# Plot model performance metrics
def plot_model_performance(results_dict):
    """Plot RMSE and R^2 values for models."""
    models = list(results_dict.keys())
    rmse_values = [results_dict[model]['rmse'] for model in models]
    r2_values = [results_dict[model]['r2'] for model in models]

    # Bar chart for RMSE
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.bar(models, rmse_values, color='skyblue')
    plt.title('RMSE of Models')
    plt.ylabel('RMSE')
    plt.xlabel('Model')

    # Bar chart for R^2
    plt.subplot(1, 2, 2)
    plt.bar(models, r2_values, color='salmon')
    plt.title('R^2 of Models')
    plt.ylabel('R^2')
    plt.xlabel('Model')

    plt.tight_layout()
    plt.show()

# Create map of Airbnb listings with nearby landmarks
def plot_airbnb_map(enriched_data):
    # Add landmarks using Google Places API
    enriched_data = add_landmarks_to_data(enriched_data)

    # Create a map centered around NYC
    nyc_map = folium.Map(location=[40.7128, -74.0060], zoom_start=12)

    # Add Airbnb properties and their nearby landmarks to the map
    for index, row in enriched_data.iterrows():
        # Define marker color based on price range
        color = 'green' if row['price'] < 100 else 'orange' if row['price'] < 200 else 'red'
        
        # Add Airbnb property marker
        folium.Marker(
            [row['latitude'], row['longitude']],
            popup=f"{row['address']} - Price: ${row['price']}",
            icon=folium.Icon(color=color)
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
