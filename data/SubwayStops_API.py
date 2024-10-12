from configparser import ConfigParser
import requests
import json
import pandas as pd

config = ConfigParser()
config.read('../config.ini')

# save output to
csv_file_path = config['DATA_SOURCES']['subway_csv']

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
    write_csv(data, csv_file_path + '.csv')
