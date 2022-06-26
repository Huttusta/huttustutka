import json
import re
import requests
from bs4 import BeautifulSoup


URL = 'https://www.alko.fi/myymalat-palvelut'
ALKO_ADDRESSES_PATH = 'static/alko_addresses.json'


def run():
    response = requests.get(URL)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    stores = []
    store_rows = soup.find_all('div', attrs={
        'class': 'column details tiny-6 medium-3 large-3'
    })

    for row in store_rows:
        store_id = re.search(r'/(\d+)\?', row.a['href'])[1]
        name = row.a.span.text
        address_spans = row.find_all('span', attrs={'class': 'address-data'})

        stores.append({
            'id': store_id,
            'name': name,
            'address': f'{address_spans[0].text} {address_spans[1].text}'
            .replace('\u00a0\n', ' ')
        })

    with open(ALKO_ADDRESSES_PATH, 'w') as f:
        json.dump(stores, f)


if __name__ == "__main__":
    run()
