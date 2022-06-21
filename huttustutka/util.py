import re
import json
from flask import url_for

ALKO_COORDINATES_PATH = 'static/alko_coordinates.json'
HUTTUSUKOT = [
    "huttusukko10.png",
    "huttusukko20.png",
    "huttusukko30.png",
    "huttusukko40.png",
    "huttusukko50.png",
]
TRESHOLDS = [5, 10, 30, 50]


def find_store_with_coordinates(store_id, coordinates):
    for store in coordinates:
        if store['id'] == store_id:
            return store

    return None


def check_huttunen(huttuset):
    with open(ALKO_COORDINATES_PATH, 'r') as f:
        alko_coordinates = json.load(f)

    res = []

    for h in huttuset:
        store = find_store_with_coordinates(h['id'], alko_coordinates)

        if not store or 'latitude' not in store:
            continue

        try:
            lower_bound = int(h['amount'])
        except ValueError:
            lower_bound = int(re.search(r'^(\d+)-', h['amount'])[1])

        if lower_bound <= TRESHOLDS[0]:
            huttusukko = HUTTUSUKOT[0]
        elif lower_bound <= TRESHOLDS[1]:
            huttusukko = HUTTUSUKOT[1]
        elif lower_bound <= TRESHOLDS[2]:
            huttusukko = HUTTUSUKOT[2]
        elif lower_bound <= TRESHOLDS[3]:
            huttusukko = HUTTUSUKOT[3]
        else:
            huttusukko = HUTTUSUKOT[4]

        res.append({
            "icon": url_for("static", filename=huttusukko),
            "lat": store['latitude'],
            "lng": store['longitude'],
            "infobox": f'{store["name"]} Huttusta {h["amount"]} kpl.',
            "scale": 0.1
        })

    return res
