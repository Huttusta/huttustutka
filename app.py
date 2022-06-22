import os
from flask import Flask
from flask import render_template
from huttustutka.scrape_huttunen import ScrapeHuttunen
from huttustutka.util import check_huttunen, get_products

app = Flask(__name__)
scraper = ScrapeHuttunen()
HUTTUNEN_ID = '003732'


@app.route('/')
def hello_huttunen():
    # huttunen = Map(
    #     identifier="huttunen",
    #     varname="huttunen",
    #     lat=60.1707368,
    #     lng=24.9347073,
    #     zoom=10,
    #     markers=check_huttunen(huttuset)
    # )

    return render_template(
        "index.html",
        products=get_products(),
        google_api_key=os.environ['GOOGLE_API_KEY'],
    )


@app.route('/<product_id>')
def get_markers(product_id):
    huttuset = scraper.how_much_huttunen(product_id)

    return check_huttunen(huttuset)


if __name__ == "__main__":
    app.run(debug=True)
