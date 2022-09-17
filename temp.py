from flask import Flask


app = Flask(__name__)


@app.route("/")
def function():
    return "Some Text"


app.run()
