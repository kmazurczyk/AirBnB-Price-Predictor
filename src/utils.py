import pandas as pd
from geopy.distance import geodesic

# Function to calculate distance between two latitude/longitude points
def calculate_distance(coord1, coord2):
    """
    Calculate the distance between two lat/lon coordinates in kilometers.
    """
    return geodesic(coord1, coord2).kilometers

# Load data with basic error handling
def load_csv(filepath):
    """
    Load a CSV file into a pandas DataFrame.
    """
    try:
        return pd.read_csv(filepath)
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return None
    except pd.errors.EmptyDataError:
        print("Empty data file.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Function to save data with error handling
def save_csv(dataframe, filepath):
    """
    Save a pandas DataFrame to a CSV file.
    """
    try:
        dataframe.to_csv(filepath, index=False)
    except Exception as e:
        print(f"An error occurred while saving file: {e}")

# Function to filter a DataFrame by column value
def filter_by_column(df, column, value):
    """
    Filter a DataFrame to only rows where the column matches the given value.
    """
    return df[df[column] == value]

# Helper function for setting up the environment variables
import os
from dotenv import load_dotenv

def load_env():
    """
    Load environment variables from a .env file.
    """
    load_dotenv()
    api_key = os.getenv("API_KEY")
    if not api_key:
        print("API key not found. Check .env file.")
    return api_key
