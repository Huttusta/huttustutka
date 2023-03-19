import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

import geocoder

ALKO_ADDRESSES_PATH = 'resources/alko_addresses.json'
ALKO_COORDINATES_PATH = 'resources/alko_coordinates.json'


def run():
    with open(ALKO_ADDRESSES_PATH, 'r') as fa:
        stores = json.load(fa)

    with requests.Session() as session:
        for idx, store in enumerate(stores):
            osm = geocoder.google(store['address'], session=session, region='fi')

            if not osm.latlng:
                print('No features found!')
                print('address:', store['address'])
                continue

            stores[idx]['latitude'] = osm.latlng[0]
            stores[idx]['longitude'] = osm.latlng[1]

    with open(ALKO_COORDINATES_PATH, 'w') as fc:
        json.dump(stores, fc)


if __name__ == "__main__":
    run()
