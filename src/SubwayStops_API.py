from configparser import ConfigParser
from datetime import date, timedelta
import time
import requests
import json
import pandas as pd
import os

# SEARCH FOR AND SAVE FILES WITH RESPECT TO ROOT PROJECT FOLDER
def get_base_path():
    cwd = os.path.basename(os.getcwd())
    if cwd.lower() != 'airbnb-price-predictor':
        return os.path.dirname(os.getcwd())
    else:
        return os.getcwd()

config = ConfigParser()
config_path = get_base_path() + '/config.ini'
# print("configuring from", config_path)
config.read(config_path)

# FILE I/O
data_dir = get_base_path() + config['DATA_SOURCES']['data_dir']
csv_file_name = config['DATA_SOURCES']['subway_csv']

def call_api():

    # set up connection
    
    url = 'https://data.ny.gov/resource/39hk-dx4f.json'
    headers = {'X-App-Token': config['OPEN_DATA_NYC']['token']}

    try:
        r = requests.get(url=url, headers=headers)
        if r.status_code == 200:
            data = pd.DataFrame(json.loads(r.text))
            data['last_modified'] = r.headers['Last-Modified']
        else:
            print(r.status_code)
            print(r.headers)
            print(r.text)
        return data

    except Exception as error:
        print(error)   

def write_csv(df, file_path):
    df.to_csv(file_path)
    print("data written to",file_path)

if __name__ == '__main__':
    data = call_api()
    write_csv(data, data_dir + csv_file_name + '.csv')
