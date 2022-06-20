import os
from flask import Flask
from flask import render_template
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from huttustutka.scrape_huttunen import ScrapeHuttunen
from huttustutka.util import check_huttunen

app = Flask(__name__)
GoogleMaps(app, key=os.environ["GOOGLE_API_KEY"])

@app.route('/')
def hello_huttunen():
    scraper = ScrapeHuttunen()
    huttuset = scraper.how_much_huttunen()

    huttunen = Map(
        identifier="huttunen",
        varname="huttunen",
        lat=60.1707368,
        lng=24.9347073,
        zoom=10,
        markers=check_huttunen(huttuset)
    )
    return render_template("index.html", huttunen=huttunen)


if __name__ == "__main__":
    app.run(debug=True)
