from bs4 import BeautifulSoup
import requests
import string
import time
from geopy.geocoders import GoogleV3
from geopy.distance import distance
from itertools import product

# Get Tesla Supercharger Map page.
response = requests.get('https://www.teslamotors.com/findus/list/superchargers/United+States')

supercharger_html = response.text

soup = BeautifulSoup(supercharger_html, 'html.parser')

superchargers_markup = soup.select('.adr')
addresses = []
geocoder = GoogleV3()

for s in superchargers_markup:
    address_parts = filter(lambda s: s is not None, [
        s.select_one('.street-address').string,
        s.select_one('.extended-address').string,
        s.select_one('.locality').string])
    full_address = ', '.join(map(lambda s: string.strip(s), address_parts))
    location = geocoder.geocode(full_address)
    time.sleep(0.1)
    
    try:
        addresses.append((location.latitude, location.longitude))
    except AttributeError:
        print 'Could not find coordinates for {}'.format(full_address)

address_pairs = product(addresses, addresses)
distances = map(lambda p: distance(p[0], p[1]).miles, address_pairs)

print 'Minimum distance between any two Superchargers is {} miles'.format(
    min(distances))


