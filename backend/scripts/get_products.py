from datetime import datetime
import json
import re
import requests
from bs4 import BeautifulSoup, SoupStrainer


URL = 'https://www.alko.fi/tuotteet/tuotelistaus/'
PARAMS = {
    "PageNumber": 967,  # 967
    "SearchTerm": "*",
    "PageSize": 12,
}
ALKO_PRODUCTS_PATH = f'resources/products-{datetime.now()}.json'


def run():
    start = datetime.now()

    response = requests.get(URL, params=PARAMS)
    response.raise_for_status()

    data_time = datetime.now()
    print(f"Datan haku kesti {data_time - start}")

    only_divs = SoupStrainer('div')
    soup = BeautifulSoup(
        response.text,
        'lxml',
        parse_only=only_divs
    )

    products = []
    product_divs = soup.find_all(
        'div',
        attrs={
            "class": "product-data-container",
            "data-alkoproduct": True
        }
    )

    for div in product_divs:
        products.append({
            'id': div["data-alkoproduct"],
            'name': div.a["title"],
        })

    print(f"Datan käsittelyssä kesti {datetime.now() - data_time}")
    print(f"Koko operaatiossa kesti {datetime.now() - start}")
    print(f"Ladattu {len(product_divs)} tuotetta")

    with open(ALKO_PRODUCTS_PATH, 'w') as f:
        json.dump(products, f)


if __name__ == "__main__":
    run()
