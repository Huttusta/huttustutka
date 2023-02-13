import re
from bs4 import BeautifulSoup
import requests

HUTTUNEN_ID = "003732"


class ScrapeHuttunen():
    def __init__(self):
        self.domain = "https://www.alko.fi/"
        self.product_path = "INTERSHOP/web/WFS/Alko-OnlineShop-Site/fi_FI/-/EUR/ViewProduct-Include?SKU="
        self.default_product_id = HUTTUNEN_ID
        self.product_details_path = "tuotteet/"

    def product_url(self, product_id):
        return f"{self.domain}{self.product_path}{product_id}"

    def product_details_url(self, product_id):
        return f"{self.domain}{self.product_details_path}{product_id}"

    def how_much_huttunen(self, product_id=None):
        if product_id is None:
            product_id = self.default_product_id

        response = requests.get(self.product_url(product_id))
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        stores = []
        a = soup.find_all("a", attrs={"data-store-item": True})

        for store in a:
            store_id = re.search(r"StoreID=(\d+)&", store["data-url"])[1]
            data = store.find_all("span")
            matches = re.findall(r"\d+", data[1].text)
            stores.append({
                "id": store_id,
                "min": matches[0],
                "max": matches[1] if len(matches) == 2 else matches[0],
            })

        return stores

    def get_product_details(self, product_id=None):
        if product_id is None:
            product_id = self.default_product_id

        response = requests.get(self.product_details_url(product_id))
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        details = dict()
        span = soup.find_all("span", attrs={"class": "js-price-container"})

        details["price"] = span[0]["content"]

        return details
