from collections import defaultdict
from configparser import ConfigParser
from datetime import date, timedelta, time
from geopy import geocoders
from matplotlib import pyplot as plt
import folium
import geopandas as gpd
import numpy as np
import pandas as pd
import json
import os
import sys
import requests

# UPDATE SEARCH PATH
base = os.getcwd()
for root, dirs, files, rootfd in os.fwalk(base, topdown=False):
    if not any(i in root for i in ['env', '.git']):
            sys.path.append(root)

# CONFIGURE SECRETS
try:
    config = ConfigParser()
    config.read('../config.ini')
except Exception as error:
    print('could not configure')
    print(error)