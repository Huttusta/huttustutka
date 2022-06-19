from flask import Flask
from flask import render_template
from flask import url_for
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import os

app = Flask(__name__)
GoogleMaps(app, key=os.environ["GOOGLE_API_KEY"])

@app.route('/')
def hello_huttunen():
    huttunen = Map(
            identifier="huttunen",
            varname="huttunen",
            lat=60.1707368,
            lng=24.9347073,
            zoom=10,
            markers=[
                {
                    "icon": url_for("static", filename="huttusukko40.png"),
                    "lat": 60.1706704,
                    "lng": 24.9348711,
                    "infobox": "asdasd",
                    "scale": 0.1
                }
            ]
    )
    return render_template("index.html", huttunen=huttunen)

if __name__ == "__main__":
    app.run(debug=True)
