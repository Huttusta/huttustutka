import re
from bs4 import BeautifulSoup
import requests


class ScrapeHuttunen():


    def __init__(self):
        self.domain = 'https://www.alko.fi/'
        self.product_path = 'INTERSHOP/web/WFS/Alko-OnlineShop-Site/fi_FI/-/EUR/ViewProduct-Include?SKU='


    def product_url(self, product_id):
        return f'{self.domain}{self.product_path}{product_id}'


    def how_much_huttunen(self, product_id):

        response = requests.get(self.product_url(product_id))
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        stores = []
        a = soup.find_all('a', attrs={'data-store-item': True})

        for store in a:
            store_id = re.search(r'StoreID=(\d+)&', store['data-url'])[1]
            data = store.find_all('span')
            stores.append({
                'id': store_id,
                'amount': data[1].text,
            })

        return stores
