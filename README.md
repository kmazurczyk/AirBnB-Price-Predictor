# AirBnB-Price-Predictor

## Contributors
Kori Thompson
Dawnena Key
Kai Mazurczyk

## Project Overview

### Problem Definition
This project aims to predict the price of Airbnb listings in NYC based on proximity to key landmarks, as well as other features such as the number of people it can accommodates, the number of bedrooms, and minimum nights required for the listing.

### Project Goal
The objective of this project is to build a model that can accurately predict Airbnb listing prices in NYC. This involves analyzing features such as proximity to key landmarks, accommodations, and other listing attributes.

### Real-world Impact
Preferences among those traveling are shifting with higher percentages opting to stay in vacation rentals over traditional accommodations like hotels. With the vacation rental market expected to continue growing, more people are choosing to host their properties on online vacation rental websites such as Airbnb. As demand for short-term rentals continues to grow, competition among hosts for bookings will further intensify. With the industry becoming more saturated with new listings, pricing rental properties has become more complicated. Accurate price prediction allows hosts to adjust rates based on demand, location, and amenities, potentially increasing booking rates and profitability. Insights gained from this model could also be valuable to rental platforms and pricing strategy consultants.

## Stack / Dependencies

* Dependencies may be installed from requirements.txt. Models prominently rely on scikit-learn.
* A .env file with valid API keys for Google Cloud and OpenData NYC is required for data extraction. Alternatively, refer to the data repo under Data Sources.

## Data Sources & Initial EDA

### Overview
We sampled 25,000 Airbnb listings in NYC with various features, including data on accommodations, amenities, location, and distances to subway stops and 30 famous NYC landmarks. Samples are weighted by borough as the distribution of listing across the boroughs was inconsistent.


**Data Repo**
CSVs supporting EDA and modeling may be found here. The main training set is *airbnb_sample_landmarks_mta_zipcodes.csv*
https://drive.google.com/drive/folders/1uFq5dFdvqfkvqRevrNPtnhqbxjgidESB?usp=sharing

### Key Features
- **Listing Features**: Accommodations, bedrooms, minimum nights, and instant booking options.
- **Location Data**: Latitude, longitude, and zip code.
- **Landmark Proximity**: Distances to notable NYC landmarks (e.g., Central Park, Brooklyn Museum).

**Variables List**
https://docs.google.com/spreadsheets/d/19CzocczwxC_jQyxzuoXsZOUjw-NxFBlo/edit?usp=share_link&ouid=114532325739400501424&rtpof=true&sd=true

### Data Limitations
* The dataset had missing values (zipcode). These were filled using Google Geocoder.
* Certain boroughs had limited samples, which could affect model performance and generalizability. 
* Outlier and non-normal distributions were prevalent across most features, which were treated during pre-processing.

Data sourcing and preprocessing may be found under **/src** and in the file **/notebooks/Airbnb_Data_Preprocessing**.
EDA may be found under **/notebooks**.

### References

* Inside AirBNB - Pre-scraped AirBNB listing data from AirBNB.com (CSV)
    * https://insideairbnb.com/

* OpenData NYC - APIs providing local transit detail as well as zip code and neighborhood geography
    * https://data.cityofnewyork.us/City-Government/Borough-Boundaries/tqmj-j8zm
    * https://data.cityofnewyork.us/Health/Modified-Zip-Code-Tabulation-Areas-MODZCTA-/pri4-ifjk/data
    * https://data.ny.gov/Transportation/MTA-Subway-Stations/39hk-dx4f/about_data

* Google Geoencoder - look up latitude/longitude for famous NYC landmarks, look up zipcode for AirBNB listings
    * https://developers.google.com/maps/documentation/geocoding/overview

## Data Cleaning & Pre Processing

Several variables were highly skewed, most noteably
* AirBNB listing price, our main predictor
* The minimum number of nights required for a booking
* Distances to nearby landmarks
    
We log scaled price and sqrt scaled each distance variable to support the data requirements of GLM models. We also removed the top 0.99 percentile of outliers.

## Feature Engineering

* **Nearby Landmarks & Transit** We used the latitude and longitude of AirBNBs, subway stops, and landmarks to identify attractions and transit nearby. We measured their distances, counted landmarks within walking distance, and identified distance to nearest transit.

* **One Hot Encoding** We one-hot encoded factors like borough and zipcode, and created binary variables for property amenities like wifi, pet policy, etc.

## Modeling

We trialed and tuned several regression models.

* GLMs: OLS, SGD, Lasso and Polynomial Lasso
* Trees: Decision tree, random forest

The data was split into training and testing sets (80-20 split). Each model's performance was assessed using the R-Squared and RSME score from cross-validation. After tuning and cross-validation, each model performed similarly with approximate 0.6 mean R2 during training.

Detailed training results can be found under **/models**.

## Key Insights

* Each model favored features related to AirBNB size over AirBNB amenities, with  three variables consistently appearing:
    * accommodates
    * bedrooms
    * bathrooms
* Proximity to landmarks generally appeared as top features over neighborhoods or zipcodes. 
* Specific landmarks varied across models. We believe these geographic features are inherently non-independent. ie Distance from the High Line ranked as a top feature in our winning Random Forest model. However, it cannot be neglected that this feature is situated in Chelsea, one of the most lucrative neighborhoods in Manhattan, and has its own zipcode, 10011. Further engineering would help us understand these variables' true contribution.

The agreement between the models on the features of importance highlights some key insights. The three most important features of the random forest model were the number of people the listing could accommodate, the number of bedrooms, and the number of bathrooms. Of relatively little importance in the model were amenities such as having Wi-Fi or a gym on the premises. The same finding was also seen to a lesser extent in the lasso regressions. This implies that the size of the listing overshadows the amenities available. The amenities may be an additional feature that helps to determine a price, but the size of the accommodation has a greater role in determining a competitive price. The greater importance placed on the listing’s proximity to landmarks rather than its location in terms of borough or zip code implies that proximity to landmarks matters in determining pricing. Some additional features that had importance in the models were the minimum number of nights for a booking, whether the listing had a license/permit/registration number, and whether the listing was instantly bookable. Similarly, the random forest also found the number of listings that a host had in NYC was important. This implies that bookings that are more commercialized may have higher prices as well and could be an area for further examination. 

## Final Result

We validated Polynomial Lasso and Random Forest as our two top competing models. Each attained 0.65 validation R2. We chose the Random Forest as our final model due to its simplicity and explainability over Polynomial regression.

### Opportunities / Future Work

Our model provides a moderately effective prediction of Airbnb listing prices in NYC. We believe the remaining gap in prediction power may be due to additional outliers that need to be analyzed and treated, and due to non-independence of geographic variables that could benefit from further engineering. 

Future steps could also include further exploring non-linear models, given the challenges within the distributions it would be interesting to try an outlier resistant clustering method like DBSCAN. 

We also evaluated this data point in time - collecting additional data and evaluating as a time series could illuminate interesting trends and potentially enhance prediction accuracy. There is also opportunity to generate features that illuminate market competition, like number of AirBNBs nearby.

### Problems

We initially sought to add AirBNB property value, square footage, type of residence, age of building, evidence of renovations from civic property valuations data. However both AirBNB and civic property datasets are intentionally anonymised to protect property owners. We were not able to tie data points to specific listings. We were also unable to take advantage of the random forest's robustness to outliers as our sample size was not large enough to overwhelm the outliers present. 


