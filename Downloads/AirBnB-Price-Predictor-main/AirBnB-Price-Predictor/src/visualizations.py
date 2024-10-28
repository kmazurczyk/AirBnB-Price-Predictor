# visualization.py
import folium
import pandas as pd
import matplotlib.pyplot as plt
from data.google_api import find_nearby_places  # Ensure this is correctly implemented and imports correctly

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
def create_map(data):
    nyc_map = folium.Map(location=[40.7128, -74.0060], zoom_start=12)

    # Add Airbnb properties and their nearby landmarks to the map
    for index, row in data.iterrows():
        # Add Airbnb property marker
        folium.Marker(
            [row['latitude'], row['longitude']],
            popup=f"{row['address']} - Price: ${row['price']}",
            icon=folium.Icon(color='blue')
        ).add_to(nyc_map)

        # Add each landmark as a separate marker
        if row['landmarks_nearby']:
            for landmark in row['landmarks_nearby']:
                # Assuming landmarks are nearby, offset slightly for better visibility (replace with actual landmark lat/long if available)
                folium.Marker(
                    [row['latitude'] + 0.001, row['longitude'] + 0.001],
                    popup=landmark.get('name', 'Landmark'),  # Use the landmark's name
                    icon=folium.Icon(color='green')
                ).add_to(nyc_map)

    # Save the map to an HTML file for visualization
    nyc_map.save('output/nyc_airbnb_landmarks_map.html')
    print("Map with Airbnb properties and landmarks saved as 'output/nyc_airbnb_landmarks_map.html'")

# Plot model performance results
def plot_results(dt_results, rf_results, glm_results):
    """Plot RMSE and R-squared values for different models."""
    models = ['Decision Tree', 'Random Forest', 'GLM']
    rmse_values = [dt_results['rmse'], rf_results['rmse'], glm_results['rmse']]
    r2_values = [dt_results['r2'], rf_results['r2'], glm_results['r2']]

    # Plot RMSE values
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.bar(models, rmse_values, color='skyblue')
    plt.title('RMSE by Model')
    plt.ylabel('RMSE')

    # Plot R-squared values
    plt.subplot(1, 2, 2)
    plt.bar(models, r2_values, color='lightgreen')
    plt.title('R-squared by Model')
    plt.ylabel('R-squared')

    plt.tight_layout()
    plt.show()

# Generate the map
create_map(airbnb_data)

