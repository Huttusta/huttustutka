from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_caching import Cache
from .scrape_huttunen import ScrapeHuttunen

app = Flask(__name__)
api = Api(app)
CORS(app)
cache = Cache(config={
    'CACHE_TYPE': 'SimpleCache',
    # results are cached one day
    'CACHE_DEFAULT_TIMEOUT': 86400,
})
cache.init_app(app)

scraper = ScrapeHuttunen()


class Amounts(Resource):
    @cache.cached()
    def get(self, product_id):
        return scraper.how_much_huttunen(product_id)

class Details(Resource):
    @cache.cached()
    def get(self, product_id):
        return scraper.get_product_details(product_id)

api.add_resource(Amounts, '/api/amounts/<string:product_id>/')
api.add_resource(Details, '/api/details/<string:product_id>/')
