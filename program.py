from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy

import requests

import sys
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
db = SQLAlchemy(app)


class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(50), unique=True)
    # temperature = db.Column(db.Integer)
    # weather_state = db.Column(db.String(50))


db_path = os.path.join("/", "weather.db")
if not os.access(db_path, os.F_OK):
    db.create_all()


db_is_empty = False



@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        from_db = Weather.query.all()

        result = []
        for entry in from_db:
            city_name = entry.city_name
            api_id = "24034c2fc253da6475cd74bc0b96cf5a"
            api_link = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&APPID={api_id}"
            dict_with_info = requests.get(api_link).json()

            city = dict_with_info["name"]
            temperature = int(dict_with_info["main"]["temp"]) - 273
            state = dict_with_info["weather"][0]["main"]
            result.append({"city_name": city, "temperature": temperature, "state": state})

        return render_template('index.html', info=result, x=from_db)
    elif request.method == "POST":
        city_name = request.form["city_name"]

        new_entry = Weather(city_name=city_name)
        db.session.add(new_entry)
        db.session.commit()
        # from_db = Weather.query.all()

        return redirect("/")





# don't change the following way to run flask:
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
