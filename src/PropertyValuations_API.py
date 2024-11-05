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
csv_file_name = config['DATA_SOURCES']['valuations_csv']

# SET DATA FILTERS

# DATE FILTER
# property valuations are dated for the coming fiscal year 
# ie, data dated 2025 will reflect 2024 valuation, and data dated 2024 was assessed in 2023
today = date.today()
this_year = today.year
next_year = this_year + 1

# FINAL ASSESSMENTS ONLY
final_assessments = 'period = 3'

# RESIDENCES FILTERS
# zoning codes
zones = 'starts_with(zoning,\"R\")'

# building class codes   
try:
    df = pd.read_csv(data_dir + config['DATA_SOURCES']['nyc_building_codes_csv']+'.csv')
    building_class_codes = df.loc[df['IS_RESIDENTIAL']==1,'BUILDING_CODE'].unique().tolist()
    building_classes = f'bldg_class in {tuple(building_class_codes)}'

except Exception as e:
    print(e)
    building_classes = '1=1'

def call_api(borough,upper_limit=500):

    # set up connection
    url = 'https://data.cityofnewyork.us/resource/8y4t-faws.json'
    headers = {'X-App-Token': config['OPEN_DATA_NYC']['token']}

    valuations_data = pd.DataFrame()
    i = 0
    batch = 1000

    print(f"Collecting valuations for borough {str(borough)}")

    while i <= upper_limit:
        time.sleep(2)
        payload = {
            '$select': 'parid, boro, block, lot, year, housenum_lo, housenum_hi, units, coop_apts, aptno, street_name, zip_code, owner, land_area, yrbuilt, yralt1_range, yralt2_range, num_bldgs, bld_story, gross_sqft, zoning, bldg_class, curmkttot, period, newdrop, noav, valref',
            '$limit': batch,
            '$where': f'{zones}' \
                + ' and ' + f'{building_classes}'
                + ' and ' + f'{final_assessments}' 
                + ' and ' + f'boro = {str(borough)}' 
                + ' and ' + f'year = \"{str(next_year)}\"',
                # f'(year = \"{str(this_year)}\" or year = \"{str(next_year)}\")',
            '$order': 'parid',
            '$offset': i * batch
            }

        try:
            r = requests.get(url=url, headers=headers, params=payload)
            if r.status_code == 200:
                data = json.loads(r.text)
                new_df = pd.DataFrame(data)
                valuations_data = pd.concat([valuations_data, new_df], ignore_index=True)
            else:
                print(r.status_code)
                print(r.headers)
                print(r.text)
                break
            print(f"page {i}")
            i += 1
            valuations_data['last_modified'] = r.headers['Last-Modified']

        except Exception as e:
            print(e)
            pass

    return valuations_data

def write_csv(df, file_path):
    df.to_csv(file_path)
    print("data written to",file_path)

if __name__ == '__main__':
    for borough in range(1,6):
        data = call_api(borough)
        write_csv(data, data_dir + csv_file_name + str(borough) + '.csv')
