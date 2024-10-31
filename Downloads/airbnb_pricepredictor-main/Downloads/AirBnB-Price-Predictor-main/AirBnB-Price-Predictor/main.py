import pandas as pd
from sklearn.model_selection import cross_validate
from sklearn.metrics import make_scorer, mean_squared_error, r2_score
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from src.feature_engineering import prepare_features, tokenize_and_clean_description, extract_description_features
from src.visualizations import plot_results
from src.google_api import geocode_address, find_nearby_places
from data.nyc_data import load_nyc_data
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Load Airbnb data path
airbnb_data_path = os.getenv("AIRBNB_DATA_PATH")

def main():
    print("Step 1: Load cleaned Airbnb data...")
    try:
        airbnb_data = pd.read_csv("data/airbnb_listings_cleaned.csv")
        print("Loaded Airbnb data successfully.")
    except FileNotFoundError:
        print("Error: Airbnb listings data file not found.")
        return

    print("Step 2: Load property valuations and MTA data...")
    try:
        property_data = pd.read_csv("data/property_valuations.csv")
        mta_data = pd.read_csv("data/MTA_data.csv")
        nyc_zip_codes, nyc_boroughs = load_nyc_data()
        print("Property, MTA, and NYC data loaded.")
    except FileNotFoundError as e:
        print(f"Error loading data files: {e}")
        return

    print("Step 3: Starting feature engineering...")
    try:
        airbnb_data = tokenize_and_clean_description(airbnb_data)
        airbnb_data = extract_description_features(airbnb_data)
        enriched_data = prepare_features(airbnb_data, property_data, mta_data, nyc_zip_codes, nyc_boroughs)
        print("Feature engineering completed.")
    except Exception as e:
        print(f"Error during feature engineering: {e}")
        return

    # Prepare data for model training
    print("Splitting data into features and target variable...")
    X = enriched_data.drop("price", axis=1)
    y = enriched_data["price"]

    # Scoring metrics
    scoring = {
        'r2': make_scorer(r2_score),
        'rmse': make_scorer(mean_squared_error, squared=False)
    }

    # Train Decision Tree model with cross-validation
    print("Training Decision Tree with cross-validation...")
    dt_model = DecisionTreeRegressor(random_state=42)
    dt_cv_results = cross_validate(dt_model, X, y, cv=5, scoring=scoring, return_train_score=True)
    dt_results = {
        'rmse': dt_cv_results['test_rmse'].mean(),
        'r2': dt_cv_results['test_r2'].mean()
    }

    # Train Random Forest model with cross-validation
    print("Training Random Forest with cross-validation...")
    rf_model = RandomForestRegressor(random_state=42)
    rf_cv_results = cross_validate(rf_model, X, y, cv=5, scoring=scoring, return_train_score=True)
    rf_results = {
        'rmse': rf_cv_results['test_rmse'].mean(),
        'r2': rf_cv_results['test_r2'].mean()
    }

    # Display results
    print("\n--- Decision Tree Results ---")
    print(f"Average RMSE: {dt_results['rmse']:.2f}, Average R^2: {dt_results['r2']:.2f}")
    print("\n--- Random Forest Results ---")
    print(f"Average RMSE: {rf_results['rmse']:.2f}, Average R^2: {rf_results['r2']:.2f}")

    # Save predictions and enriched data
    print("Saving predictions and enriched data...")
    enriched_data['predicted_price'] = rf_model.fit(X, y).predict(X)  # Fitting and predicting for the full data
    enriched_data.to_csv("data/airbnb_price_predictions.csv", index=False)
    print("Predictions saved to 'data/airbnb_price_predictions.csv'.")

if __name__ == '__main__':
    main()
