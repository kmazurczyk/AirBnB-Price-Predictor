from dotenv import load_dotenv
from __init__ import get_base_path
import pandas as pd
import sys
import os

"""
weighted sample of the cleansed AirBNB dataset

input: airbnb_listings_cleaned.csv
output: airbnb_sample.csv

weight_boroughs(df, latest_period = True) 
- modifies df by applying a "frequencies" column - count of listings in each borough. 
- when latest_period = True, it will also drop duplicate listings keeping latest period, and reweighting accordingly

sample_df(df, n=25000, weights='frequencies', random_state = 42)
- will take 25,000 samples based on weight_boroughs(), unless another parameter is passed

"""

# environment
load_dotenv(get_base_path() + '/airbnb.env')
data_dir = get_base_path() + os.getenv('data_dir')

# read AirBNB CSV
def read_csv(file_csv='Airbnb_listings_cleaned.csv'):
    try:
        file_path = data_dir + 'processed/' + file_csv
        df = pd.read_csv(file_path, index_col=0)
        return df

    except FileNotFoundError:
        print(f"Could not find {file_csv}. Expected path: {file_path}")
    
    except Exception as e:
        print(e)

# calc weights by borough
def weight_boroughs(df,latest_period=True):

    # undo dummies in single column "boroughs"
    df['boroughs'] = df.filter(like='neighbourhood_group_cleansed_').idxmax(axis=1).str.replace('neighbourhood_group_cleansed_', '')

    # calc weights/create sample either from latest period, or all the data
    if latest_period:
        df.sort_values(['id','last_scraped'], inplace=True)
        df.drop_duplicates(subset=['id'],keep='last',inplace=True)

    # calc frequencies to be used as weights
    frequencies = df['boroughs'].value_counts().to_dict()
    df['frequencies'] = df['boroughs'].map(frequencies)
    return df

# weighted sample
def sample_df(df, n=25000, weights='frequencies', random_state=42):
    
    # sample
    df_sample = df.sample(n=n, weights=weights, random_state=random_state)
    return df_sample

if __name__ == '__main__':
    # read cleansed Airbnb data
    df = read_csv()
    
    # calc proportions by borough
    df = weight_boroughs(df)

    # sample
    df = sample_df(df)

    # transform - drop helper columns
    print(df['boroughs'].value_counts())
    df.drop(['boroughs','frequencies'],axis=1, inplace=True)

    # save to csv
    sample_path = data_dir + 'processed/' + 'airbnb_sample.csv'
    df.to_csv(sample_path)
    print("Data written to ",sample_path)