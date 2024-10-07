from configparser import ConfigParser
from datetime import date, timedelta
import time
import requests
import json
import pandas as pd

# save output to
'ValuationsData.csv'

# set up connection
config = ConfigParser()
config.read('config.ini')
url = 'https://data.cityofnewyork.us/resource/8y4t-faws.json'
headers = {'X-App-Token': config['OPEN DATA NYC']['token']}

# we are interested in last 12 mo of data
today = date.today()
trailing_12mo = timedelta(days=365)
this_year = today.year
last_year = (today - trailing_12mo).year

valuations_data = pd.DataFrame()
i = 0
batch = 10

while i < 1:
    time.sleep(1)
    payload = {
           '$select': 'parid, boro, block, lot, year, housenum_lo, housenum_hi, street_name, zip_code, owner, land_area, yrbuilt, num_bldgs, bld_story, gross_sqft, zoning, bldg_class, curmkttot',
           '$limit': batch,
           '$where': 'starts_with(zoning,\"R\")' + ' and ' + f'(year = \"{str(this_year)}\" or year = \"{str(last_year)}\")',
           '$order': 'parid',
           '$offset': i * batch
        }

    try:
        r = requests.get(url=url, headers=headers, params=payload)
        data = json.loads(r.text)
        new_df = pd.DataFrame(data)
        valuations_data = pd.concat([valuations_data, new_df], ignore_index=True)
        i += 1

    except:
        print(response.content)

valuations_data['last_modified'] = r.headers['Last-Modified']
valuations_data.to_csv('valuations_data.csv')

if __name__ == "__main__":
    pass