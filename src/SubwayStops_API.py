from datetime import date, timedelta
from dotenv import load_dotenv
from __init__ import get_base_path
import time
import requests
import json
import pandas as pd
import os

# environment
load_dotenv(get_base_path() + '/airbnb.env')
data_dir = get_base_path() + os.getenv('data_dir')

# requests
url = 'https://data.ny.gov/resource/39hk-dx4f.json'
headers = {'X-App-Token': os.getenv("OPEN_DATA_NYC_KEY")}

def call_api():
   
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
    write_csv(data, data_dir + 'raw/' + 'SubwayStopsData' + '.csv')
