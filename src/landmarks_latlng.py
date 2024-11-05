import os
import pandas as pd
import requests
import sys
from __init__ import get_base_path
from dotenv import load_dotenv
from google_api import geocode_lat_long

'''
get latitudes and longitudes from Google GeoCoder API for landmark names 

input - CSV of landmark names
output - CSV [landmark name, latitude, longitude]
requires - Google API Key
'''

# environment
load_dotenv(get_base_path() + '/airbnb.env')
api_key = os.getenv('GOOGLE_API_KEY')
data_dir = get_base_path() + os.getenv('data_dir')

# load favorite landmarks
path = data_dir + 'raw/' + 'NYC_famous_landmarks_list' + '.csv'
df = pd.read_csv(path, header=None, names=['landmark'])

# send to google for lat long
df['lat_lng'] = df['landmark'].apply(lambda x: geocode_lat_long(x, api_key))

# transform
df[['latitude','longitude']] = pd.DataFrame(df['lat_lng'].to_list(), index = df.index)
df.dropna(inplace=True)

# save
path = data_dir + 'processed/' + 'NYC_famous_landmarks_list' + '.csv'
df[['landmark','latitude','longitude']].to_csv(path)