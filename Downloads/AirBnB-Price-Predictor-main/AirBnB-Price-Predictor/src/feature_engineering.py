import pandas as pd
from geopy.distance import geodesic
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('stopwords')

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

def tokenize_and_clean_description(data):
    """Tokenize and clean descriptions by removing stopwords."""
    stop_words = set(stopwords.words('english'))
    data['tokenized_description'] = data['description'].apply(word_tokenize)
    data['cleaned_description'] = data['tokenized_description'].apply(
        lambda tokens: [word.lower() for word in tokens if word.lower() not in stop_words]
    )
    return data
