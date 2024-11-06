import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from geopy.distance import geodesic

nltk.download('punkt')
nltk.download('stopwords')

# Load and process MTA data
def load_and_process_mta_data(mta_path):
    mta_data = pd.read_csv(mta_path)
    mta_data['stop_name'] = mta_data['stop_name'].str.strip().str.lower()  # Clean station names
    return mta_data

# Load and process Property Valuation data
def load_and_process_property_valuations(prop_path):
    prop_data = pd.read_csv(prop_path)
    prop_data.dropna(subset=['address'], inplace=True)
    return prop_data

# Calculate distances between Airbnb listings and MTA subway stations
def calculate_distance_to_nearest_station(airbnb_data, mta_data):
    distances = []
    for idx, row in airbnb_data.iterrows():
        listing_location = (row['latitude'], row['longitude'])
        min_distance = mta_data.apply(
            lambda station: geodesic(listing_location, (station['latitude'], station['longitude'])).miles,
            axis=1
        ).min()
        distances.append(min_distance)
    airbnb_data['distance_to_nearest_station'] = distances
    return airbnb_data

# Tokenization and cleaning of descriptions
def tokenize_and_clean_description(data):
    stop_words = set(stopwords.words('english'))
    data['tokenized_description'] = data['description'].apply(word_tokenize)
    data['cleaned_description'] = data['tokenized_description'].apply(
        lambda tokens: [word.lower() for word in tokens if word.lower() not in stop_words]
    )
    return data

# Feature extraction from property descriptions
def extract_description_features(data):
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

    data['description_features'] = data['cleaned_description'].apply(
        lambda tokens: extract_features(tokens, feature_keywords)
    )
    return data

# Optional: Sentiment analysis for reviews (if applicable)
def sentiment_analysis(data):
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(data['cleaned_reviews'])
    y = data['sentiment_label']  # 1 for positive, 0 for negative

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    clf = MultinomialNB()
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    return accuracy

# Primary feature preparation function
def prepare_features(airbnb_data, property_data, mta_data, nyc_zip_codes, nyc_boroughs):
    airbnb_data = calculate_distance_to_nearest_station(airbnb_data, mta_data)
    airbnb_data = pd.merge(airbnb_data, property_data, on='property_id', how='left')
    airbnb_data = pd.merge(airbnb_data, nyc_zip_codes, on='zip_code', how='left')
    airbnb_data = pd.merge(airbnb_data, nyc_boroughs, on='borough_id', how='left')
    return airbnb_data
