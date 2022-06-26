from flask import Flask
from flask_restful import Resource, Api
from .scrape_huttunen import ScrapeHuttunen

app = Flask(__name__)
api = Api(app)
scraper = ScrapeHuttunen()


# @app.route('/')
# def hello_huttunen():
#     # huttunen = Map(
#     #     identifier="huttunen",
#     #     varname="huttunen",
#     #     lat=60.1707368,
#     #     lng=24.9347073,
#     #     zoom=10,
#     #     markers=check_huttunen(huttuset)
#     # )

#     return render_template(
#         "index.html",
#         products=get_products(),
#         google_api_key=os.environ['GOOGLE_API_KEY'],
#     )


class Amounts(Resource):
    def get(self, product_id=None):
        return scraper.how_much_huttunen(product_id)


api.add_resource(Amounts, '/amounts/', '/amounts/<string:product_id>/')


if __name__ == "__main__":
    app.run(debug=True)
