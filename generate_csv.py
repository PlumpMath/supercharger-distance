# Generates the csv file everything else is built from.
# Basically a poor man's cache for the Supercharger data.

from bs4 import BeautifulSoup
import requests
import string
import time
from geopy.geocoders import GoogleV3
from geopy.distance import distance
from itertools import product
import re

def _str(s):
    if s is None:
        return ''
    else:
        return str(s)

# Get Tesla Supercharger Map page.
response = requests.get('https://www.teslamotors.com/findus/list/superchargers/United+States')

supercharger_html = response.text

soup = BeautifulSoup(supercharger_html, 'html.parser')

superchargers_markup = soup.select('.adr')
superchargers = []
geocoder = GoogleV3()

for s in superchargers_markup:
    address = ', '.join(
        filter(lambda s: len(s) > 0,
               map(_str,
                   [s.select_one('.street-address').string,
                    s.select_one('.extended-address').string])))
    locality = s.select_one('.locality').string
    full_address = ', '.join([address, locality])
    location = geocoder.geocode(full_address)
    time.sleep(0.1)  # so we don't overrun the per-second limit of the Google API.
    location_map = {'address': re.escape(address),
                    'locality': re.escape(locality)}
    try:
        location_map['lat'] = str(location.latitude)
        location_map['long'] = str(location.longitude)
    except AttributeError:
        print 'Could not find coordinates for {}'.format(full_address)
    finally:
        if 'lat' not in location_map:
            location_map['lat'] = ''
        if 'long' not in location_map:
            location_map['long'] = ''
        superchargers.append(location_map)

with open('superchargers.csv', 'w') as csv_file:
    # Write legend row.
    csv_file.write('address,locality,lat,long\n')
    for s in superchargers:
        csv_file.write(','.join([
            s['address'],
            s['locality'],
            s['lat'],
            s['long']]) + '\n')
    
