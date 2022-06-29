import json
import requests

PRODUCT_URL = "https://www.alko.fi/INTERSHOP/web/WFS/Alko-OnlineShop-Site/fi_FI/-/EUR/ViewProduct-Include?SKU="

with open("src/assets/data/alko_products_sorted.json", "r") as f:
    data = json.load(f)

new_data = []

session = requests.Session()
for product in data:
    response = session.get(f"{PRODUCT_URL}product['id']")
    print(response.text)
    break
