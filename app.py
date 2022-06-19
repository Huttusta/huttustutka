from flask import Flask
from flask import render_template
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
            lat=60.1707253,
            lng=24.9329029,
            zoom=16
    )
    return render_template("index.html", huttunen=huttunen)

if __name__ == "__main__":
    app.run(debug=True)
