import re
from bs4 import BeautifulSoup
import requests


class ScrapeHuttunen():

    def __init__(self):
        huttunen_id = '003732'
        self.url = f'https://www.alko.fi/INTERSHOP/web/WFS/Alko-OnlineShop-Site/fi_FI/-/EUR/ViewProduct-Include?SKU={huttunen_id}'

    def how_much_huttunen(self):
        response = requests.get(self.url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        stores = []
        a = soup.find_all('a', attrs={'data-store-item': True})

        for store in a:
            store_id = re.search(r'StoreID=(\d+)&', store['data-url'])[1]
            data = store.find_all('span')
            stores.append({
                'id': store_id,
                # 'name': data[0].text,
                'amount': data[1].text,
            })

        return stores


scraper = ScrapeHuttunen()

scraper.how_much_huttunen()
