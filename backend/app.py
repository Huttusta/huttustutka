from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
from .scrape_huttunen import ScrapeHuttunen

app = Flask(__name__)
api = Api(app)
CORS(app)
scraper = ScrapeHuttunen()


class Amounts(Resource):
    def get(self, product_id):
        return scraper.how_much_huttunen(product_id)


api.add_resource(Amounts, '/amounts/<string:product_id>/')
