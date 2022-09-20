from flask import Flask, request, render_template, redirect, flash
from flask_sqlalchemy import SQLAlchemy

import requests

import sys
import os

app = Flask(__name__)
app.config.from_pyfile("config.py")
db = SQLAlchemy(app)


def return_data_from_api(city_name_value):
    api_id = "24034c2fc253da6475cd74bc0b96cf5a"
    api_link = f"http://api.openweathermap.org/data/2.5/weather?q={city_name_value}&APPID={api_id}"
    return requests.get(api_link).json()

class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(50), unique=True)


db_path = os.path.join("/", "weather.db")
if not os.access(db_path, os.F_OK):
    db.create_all()


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        from_db = Weather.query.all()

        result = []
        for entry in from_db:
            # city_id = entry.id
            city_name = entry.city_name
            dict_with_info = return_data_from_api(city_name)

            city = dict_with_info["name"]
            temperature = int(dict_with_info["main"]["temp"]) - 273
            state = dict_with_info["weather"][0]["main"]
            result.append({"city_name": city, "temperature": temperature, "state": state})

        return render_template('index.html', info=result, x=from_db)
    elif request.method == "POST":
        city_name = request.form["city_name"]

        if return_data_from_api(city_name)["cod"] == "404":
            flash("The city doesn't exist!")
            return redirect("/")

        q = db.session.query(Weather.city_name).filter(Weather.city_name == city_name)
        city_in_db = db.session.query(q.exists()).scalar()

        if not city_in_db:
            new_entry = Weather(city_name=city_name)
            db.session.add(new_entry)
            db.session.commit()
        else:
            flash("The city has already been added to the list!")

        return redirect("/")


@app.route('/delete/<city_name>', methods=['GET', 'POST'])
def delete(city_name):
    city = db.session.query(Weather).filter(Weather.city_name == city_name).first()
    print(city, type(city))
    db.session.delete(city)
    db.session.commit()
    return redirect('/')


# don't change the following way to run flask:
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
