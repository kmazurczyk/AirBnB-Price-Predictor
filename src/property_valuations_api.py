from datetime import date, timedelta
from dotenv import load_dotenv
from __init__ import get_base_path
import time
import json
import pandas as pd
import os
import sys
import requests

help_text = """
            PropertyValuations_API.py
            Collects property data from OpenDataNYC API

            Required Arguments:
            batch_all                   Collect valuations for all NYC residences. Returns CSV files batched by borough.
            addresses filename.csv      Pass a CSV of addresses to lookup valuations. 
                                        It is not likely to find exact matches, returns CSV files with matches by street name and zip code.
            """

# Load environment variables from .env file
load_dotenv(get_base_path() + '/airbnb.env')

# ******* FILE I/O *********
data_dir = get_base_path() + os.getenv('data_dir')

# ******* REQUESTS *********
url = 'https://data.cityofnewyork.us/resource/8y4t-faws.json'
headers = {'X-App-Token': os.getenv("OPEN_DATA_NYC_KEY")}

# **** SET ALWAYS ON FILTERS FOR PAYLOAD ****

# DATE FILTER
# property valuations are dated for the coming fiscal year 
# ie, data dated 2025 will reflect 2024 valuation, and data dated 2024 was assessed in 2023
today = date.today()
this_year = today.year
next_year = this_year + 1

# FINAL ASSESSMENTS ONLY
final_assessments = 'period = 3'

# RESIDENTIAL PROPERTIES ONLY

# by zoning code
zones = 'starts_with(zoning,\"R\")'

# by building class code
try:
    building_codes_csv = data_dir + 'reference/' + "NYC_building_classification_codes" + '.csv'
    df = pd.read_csv(building_codes_csv)
    building_class_codes = df.loc[df['IS_RESIDENTIAL']==1,'BUILDING_CODE'].unique().tolist()
    building_classes = f'bldg_class in {tuple(building_class_codes)}'

except FileNotFoundError as f:
    print(f"Could not find building codes. Expected path: {building_codes_csv}")
    building_classes = '1=1'

# ******* API CALLS ********

# get valuations for all NYC residences from OpenDataNYC batched by borough
def call_api_batch(borough,upper_limit=500):

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

# look up valuations by address
def call_api_by_address(address_dict):

    print(f"Collecting valuations for address {address_dict}")
    # expects address_dict.keys ['housenum_lo','street_name', 'zip_code']
        
    time.sleep(2)
    payload = {
        '$select': 'parid, boro, block, lot, year, housenum_lo, housenum_hi, units, coop_apts, aptno, street_name, zip_code, owner, land_area, yrbuilt, yralt1_range, yralt2_range, num_bldgs, bld_story, gross_sqft, zoning, bldg_class, curmkttot, period, newdrop, noav, valref',
        '$where': f'{zones}' \
            + ' and ' + f'{building_classes}'
            + ' and ' + f'{final_assessments}' 
            + ' and ' + f'housenum_lo >= \"{str(address_dict["housenum_lo"]).upper()}\"'
            + ' and ' + f'street_name = \"{str(address_dict["street_name"]).upper()}\"' 
            + ' and ' + f'zip_code like \"{str(address_dict["zip_code"])}%\"'
            + ' and ' + f'year = \"{str(next_year)}\"',
            # + f'(year = \"{str(this_year)}\" or year = \"{str(next_year)}\")',
        '$order': 'parid',
        }

    try:
        r = requests.get(url=url, headers=headers, params=payload)
        if r.status_code == 200:
            data = json.loads(r.text)
            df = pd.DataFrame(data)
            df['last_modified'] = r.headers['Last-Modified']
            print(r.status_code)
            print(r.headers)
        else:
            print(r.status_code)
            print(r.headers)
            print(r.text)
        
    except Exception as e:
        print(e)
        pass

    return df

def read_addresses(file_csv):
    try:
        file_path = data_dir + 'raw/' + file_csv
        df = pd.read_csv(file_path)
    except FileNotFoundError as f:
        print(f"Could not find {file_csv}. Expected path: {file_path}")
        
def write_csv(df, file_path):
    df.to_csv(file_path)
    print("data written to",file_path)

if __name__ == '__main__':
    try:
        if sys.argv[1] == 'batch_all':
            for borough in range(1,6):
                csv_file_name = data_dir + 'raw/' + 'ValuationsData' + str(borough) + '.csv'
                data = call_api_batch(borough)
                write_csv(data, csv_file_name)
                print("data sent to", csv_file_name)

        elif sys.argv[1] == 'addresses':
            csv_file_name = data_dir + 'raw/' + 'nearest_addresses' + '.csv'
            addresses = read_addresses('test.csv')
            # data = call_api_by_address()
            # write_csv(data, csv_file_name)
            # print("data sent to", csv_file_name)

        else:
            raise Exception(help_text)
    
    except Exception as e:
        print('Expected some arguments: \n', help_text)
        print("Exception was: ", e)