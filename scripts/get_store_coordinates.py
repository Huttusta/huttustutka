import json
import requests
import geocoder

ALKO_ADDRESSES_PATH = 'static/alko_addresses.json'
ALKO_COORDINATES_PATH = 'static/alko_coordinates.json'


def run():
    with open(ALKO_ADDRESSES_PATH, 'r') as fa:
        stores = json.load(fa)

    with requests.Session() as session:
        for idx, store in enumerate(stores):
            osm = geocoder.osm(store['address'], session=session)

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
