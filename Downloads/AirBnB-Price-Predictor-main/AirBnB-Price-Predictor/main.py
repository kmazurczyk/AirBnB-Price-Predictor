import pandas as pd
from sklearn.model_selection import train_test_split
from src.feature_engineering import prepare_features, tokenize_and_clean_description, extract_description_features
from src.models import train_decision_tree, train_random_forest, train_glm
from src.visualizations import plot_results
from src.google_api import geocode_address, find_nearby_places
from data.nyc_data import load_nyc_data
from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env file

# Load environment variables
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
        print("Property data loaded.")
        mta_data = pd.read_csv("data/MTA_data.csv")
        print("MTA data loaded.")
        nyc_zip_codes, nyc_boroughs = load_nyc_data()
        print("NYC data loaded.")
    except FileNotFoundError as e:
        print(f"Error loading data files: {e}")
        return

    # Perform feature engineering
    print("Step 3: Starting feature engineering...")
    try:
        airbnb_data = tokenize_and_clean_description(airbnb_data)
        print("Tokenization and cleaning of descriptions completed.")
        
        airbnb_data = extract_description_features(airbnb_data)
        print("Feature extraction completed.")
        
        enriched_data = prepare_features(airbnb_data, property_data, mta_data, nyc_zip_codes, nyc_boroughs)
        print("All feature engineering completed.")
    except Exception as e:
        print(f"Error during feature engineering: {e}")
        return

    # Step 4: Split the enriched dataset into training and test sets
    print("Splitting data into training and testing sets...")
    try:
        X = enriched_data.drop("price", axis=1)
        y = enriched_data["price"]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        print("Data split successfully.")
    except Exception as e:
        print(f"Error during data splitting: {e}")
        return

    # Step 5: Train models and collect results
    print("Training models...")
    try:
        print("Training Decision Tree...")
        dt_results, dt_model = train_decision_tree(X_train, X_test, y_train, y_test)
        print("Decision Tree model trained.")

        print("Training Random Forest...")
        rf_results, rf_model = train_random_forest(X_train, X_test, y_train, y_test)
        print("Random Forest model trained.")

        print("Training GLM...")
        glm_results, glm_model = train_glm(X_train, X_test, y_train, y_test)
        print("GLM model trained.")
    except Exception as e:
        print(f"Error during model training: {e}")
        return

    # Step 6: Display model results
    print("Displaying model results...")
    try:
        print("\n--- Decision Tree Results ---")
        print(f"RMSE: {dt_results['rmse']:.2f}, R^2: {dt_results['r2']:.2f}")
        print("\n--- Random Forest Results ---")
        print(f"RMSE: {rf_results['rmse']:.2f}, R^2: {rf_results['r2']:.2f}")
        print("\n--- Generalized Linear Model (GLM) Results ---")
        print(f"RMSE: {glm_results['rmse']:.2f}, R^2: {glm_results['r2']:.2f}")
    except Exception as e:
        print(f"Error during results display: {e}")
        return

    # Step 7: Save predictions and enriched data
    print("Saving predictions and enriched data...")
    try:
        enriched_data['predicted_price'] = rf_model.predict(X)
        enriched_data.to_csv("data/airbnb_price_predictions.csv", index=False)
        print("Predictions saved to 'data/airbnb_price_predictions.csv'.")
    except Exception as e:
        print(f"Error during saving: {e}")
        return

if __name__ == '__main__':
    main()
