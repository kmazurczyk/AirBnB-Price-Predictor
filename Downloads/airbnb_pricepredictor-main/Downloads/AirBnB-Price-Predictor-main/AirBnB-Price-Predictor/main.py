import pandas as pd
from sklearn.model_selection import train_test_split, cross_validate
from src.feature_engineering import prepare_features, tokenize_and_clean_description, extract_description_features
from src.models import train_decision_tree, train_random_forest, train_glm
from src.visualizations import plot_price_heatmap, plot_feature_importance, plot_actual_vs_predicted, plot_cross_validation_scores, plot_price_distribution_by_borough
from src.google_api import geocode_address, find_nearby_places
from data.nyc_data import load_nyc_data
from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env file

# Load environment variables
airbnb_data_path = os.getenv("AIRBNB_DATA_PATH")

def main():
    print("Step 1: Load cleaned Airbnb data...")
    airbnb_data = pd.read_csv("data/airbnb_listings_cleaned.csv")
    # Rest of data loading and processing as in your current code...

    # Split data for training
    X = enriched_data.drop("price", axis=1)
    y = enriched_data["price"]

    # Using cross_validate for evaluation
    print("Performing cross-validation for model evaluation...")
    cv_results = cross_validate(rf_model, X, y, cv=5, scoring=('r2', 'neg_root_mean_squared_error'), return_train_score=True)
    print("Cross-validation results:")
    print("R^2 Scores:", cv_results['test_r2'])
    print("RMSE Scores:", -cv_results['test_neg_root_mean_squared_error'])

    # Model Training
    rf_results, rf_model = train_random_forest(X_train, X_test, y_train, y_test)
    
    # Visualization
    print("Generating visualizations...")
    plot_feature_importance(rf_model.feature_importances_, X.columns)
    plot_actual_vs_predicted(y_test, rf_model.predict(X_test))
    plot_cross_validation_scores(cv_results)
    plot_price_heatmap(enriched_data)
    plot_price_distribution_by_borough(enriched_data)

if __name__ == '__main__':
    main()
