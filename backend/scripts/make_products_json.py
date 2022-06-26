import csv
import json

CSV_FILE = 'static/alkon-valikoima.csv'
JSON_FILE = 'static/alko_products.json'


def run():
    with open(CSV_FILE, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        data_csv = list(csvreader)

    data_json = [
        {
            'id': product[0],
            'name': product[1],
        }
        for product in data_csv
    ]

    with open(JSON_FILE, 'w') as jsonfile:
        json.dump(data_json, jsonfile)


if __name__ == '__main__':
    run()
