import pandas as pd
from sklearn.model_selection import train_test_split
from src.feature_engineering import prepare_features, tokenize_and_clean_description, extract_description_features
from src.models import train_decision_tree, train_random_forest, train_glm
from src.visualization import plot_results
from data.google_api import geocode_address, find_nearby_places
from nyc_data import load_nyc_data
from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env file

# Load environment variables
airbnb_data_path = os.getenv("AIRBNB_DATA_PATH")

def main():
    # Step 1: Load cleaned Airbnb data
    try:
        airbnb_data = pd.read_csv("data/airbnb_listings_cleaned.csv")
        print("Loaded Airbnb data.")
    except FileNotFoundError:
        print("Error: Airbnb listings data file not found.")
        return

    # Step 2: Prepare the data by integrating property valuations and MTA data
    try:
        property_data = pd.read_csv("data/property_valuations.csv")
        mta_data = pd.read_csv("data/MTA_data.csv")
        nyc_zip_codes, nyc_boroughs = load_nyc_data()
        print("Loaded property and MTA data.")
    except FileNotFoundError as e:
        print(f"Error loading data files: {e}")
        return

    # Perform feature engineering
    airbnb_data = tokenize_and_clean_description(airbnb_data)
    airbnb_data = extract_description_features(airbnb_data)
    enriched_data = prepare_features(airbnb_data, property_data, mta_data, nyc_zip_codes, nyc_boroughs)

    # Step 3: Split the enriched dataset into training and test sets
    X = enriched_data.drop("price", axis=1)
    y = enriched_data["price"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Step 4: Train models and collect results
    dt_results, dt_model = train_decision_tree(X_train, X_test, y_train, y_test)
    rf_results, rf_model = train_random_forest(X_train, X_test, y_train, y_test)
    glm_results, glm_model = train_glm(X_train, X_test, y_train, y_test)

    # Step 5: Display model results
    print("\n--- Decision Tree Results ---")
    print(f"RMSE: {dt_results['rmse']:.2f}, R^2: {dt_results['r2']:.2f}")
    print("\n--- Random Forest Results ---")
    print(f"RMSE: {rf_results['rmse']:.2f}, R^2: {rf_results['r2']:.2f}")
    print("\n--- Generalized Linear Model (GLM) Results ---")
    print(f"RMSE: {glm_results['rmse']:.2f}, R^2: {glm_results['r2']:.2f}")

    # Step 6: Optional - Visualize results
    plot_results(dt_results, rf_results, glm_results)

    # Step 7: Save predictions and enriched data
    enriched_data['predicted_price'] = rf_model.predict(X)
    enriched_data.to_csv("data/airbnb_price_predictions.csv", index=False)
    print("\nResults saved to 'data/airbnb_price_predictions.csv'.")

if __name__ == '__main__':
    main()

