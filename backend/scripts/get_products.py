from datetime import datetime
import json
import re
import requests
from bs4 import BeautifulSoup, SoupStrainer


URL = 'https://www.alko.fi/tuotteet/tuotelistaus/'
ALKO_PRODUCTS_PATH = f'resources/products-{datetime.now()}.json'



def haeSivujenMaara():
    response1 = requests.get(URL)
    response1.raise_for_status()

    keitto = BeautifulSoup(response1.text, 'lxml')
    tuotemaararivi = keitto.find("h3", class_="product-count")

    #Selvittää tuotemäärän HTML:stä olettaen että .text palauttaa pelkkiä lukuja ja lopussa olevan sanan, joka unohdetaan.
    tuotemaara = int(''.join(tuotemaararivi.text.split()[0:-1]))

    #Yhdellä alkon sivulla on 12 tuotetta ja sivujen indeksointi alkaa nollasta.
    sivujenmaara = int(tuotemaara/12)

    return sivujenmaara


def run():
    start = datetime.now()

    sivujenmaara = haeSivujenMaara()

    PARAMS = {
        "PageNumber": sivujenmaara, 
        "SearchTerm": "*",
        "PageSize": 12,
    }

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
