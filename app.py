from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_huttunen():
    return '<h1>Huttusta :D</h1>'

if __name__ == "__main__":
    app.run(debug=True)
