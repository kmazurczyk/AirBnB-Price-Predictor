import pandas as pd
from sklearn.model_selection import train_test_split, cross_validate
from src.feature_engineering import prepare_features, tokenize_and_clean_description, extract_description_features
from src.models import train_decision_tree, train_random_forest, train_glm
from src.visualizations import plot_model_performance, plot_airbnb_map
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

    # Step 4: Split the enriched dataset into features and target
    print("Splitting data into training and testing sets...")
    try:
        X = enriched_data.drop("price", axis=1)
        y = enriched_data["price"]
        print("Data split successfully.")
    except Exception as e:
        print(f"Error during data splitting: {e}")
        return

    # Step 5: Train models using cross-validation and collect results
    print("Training models with cross-validation...")
    try:
        results_dict = {}

        print("Training Decision Tree with cross-validation...")
        dt_results = cross_validate(train_decision_tree, X, y, cv=5, scoring=('r2', 'neg_root_mean_squared_error'), return_train_score=False)
        dt_results = {'rmse': -dt_results['test_neg_root_mean_squared_error'].mean(), 'r2': dt_results['test_r2'].mean()}
        results_dict['Decision Tree'] = dt_results
        print("Decision Tree cross-validation completed.")

        print("Training Random Forest with cross-validation...")
        rf_results = cross_validate(train_random_forest, X, y, cv=5, scoring=('r2', 'neg_root_mean_squared_error'), return_train_score=False)
        rf_results = {'rmse': -rf_results['test_neg_root_mean_squared_error'].mean(), 'r2': rf_results['test_r2'].mean()}
        results_dict['Random Forest'] = rf_results
        print("Random Forest cross-validation completed.")

        print("Training GLM with cross-validation...")
        glm_results = cross_validate(train_glm, X, y, cv=5, scoring=('r2', 'neg_root_mean_squared_error'), return_train_score=False)
        glm_results = {'rmse': -glm_results['test_neg_root_mean_squared_error'].mean(), 'r2': glm_results['test_r2'].mean()}
        results_dict['GLM'] = glm_results
        print("GLM cross-validation completed.")
    except Exception as e:
        print(f"Error during model training: {e}")
        return

    # Step 6: Display model results
    print("Displaying model results...")
    try:
        for model_name, metrics in results_dict.items():
            print(f"\n--- {model_name} Results ---")
            print(f"RMSE: {metrics['rmse']:.2f}, R^2: {metrics['r2']:.2f}")
    except Exception as e:
        print(f"Error during results display: {e}")
        return

    # Step 7: Visualize model performance metrics
    plot_model_performance(results_dict)

    # Step 8: Visualize Airbnb listings with landmarks on map
    plot_airbnb_map(enriched_data)

    # Step 9: Save predictions and enriched data
    print("Saving predictions and enriched data...")
    try:
        # Use Random Forest model to make predictions
        rf_model = train_random_forest(X, y)  # Train on entire dataset for final prediction
        enriched_data['predicted_price'] = rf_model.predict(X)
        enriched_data.to_csv("data/airbnb_price_predictions.csv", index=False)
        print("Predictions saved to 'data/airbnb_price_predictions.csv'.")
    except Exception as e:
        print(f"Error during saving: {e}")
        return

if __name__ == '__main__':
    main()

