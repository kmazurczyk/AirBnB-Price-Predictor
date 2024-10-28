# feature_engineering.py
import pandas as pd
from geopy.distance import geodesic

def prepare_features(property_data, mta_data):
    """Merge property data with MTA data and calculate distance to subway."""
    # Sample merging and distance calculations
    for i, property_row in property_data.iterrows():
        min_distance = min(
            mta_data.apply(lambda mta_row: geodesic(
                (property_row['lat'], property_row['lng']),
                (mta_row['stop_lat'], mta_row['stop_lon'])
            ).meters, axis=1)
        )
        property_data.at[i, 'nearest_subway_distance'] = min_distance
    return property_data
