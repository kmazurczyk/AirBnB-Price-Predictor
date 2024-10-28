# feature_engineering.py
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

def extract_description_features(data):
    """Extract specific features from property descriptions based on keywords."""
    feature_keywords = {
        'luxury': ['luxury', 'high-end', 'premium'],
        'proximity_to_transit': ['subway', 'train', 'transit'],
        'view': ['city view', 'ocean view', 'park view']
    }

    def extract_features(tokens, feature_keywords):
        features = {}
        for feature, keywords in feature_keywords.items():
            features[feature] = any(token.lower() in keywords for token in tokens)
        return features

    # Apply extraction to each tokenized description and add as new columns
    feature_df = data['cleaned_description'].apply(
        lambda tokens: extract_features(tokens, feature_keywords)
    ).apply(pd.Series)
    
    data = pd.concat([data, feature_df], axis=1)
    return data
