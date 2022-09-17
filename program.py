from flask import Flask
from flask import request
from flask import render_template

import requests


import sys

app = Flask(__name__)

add_flag = False


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template('index.html')
    elif request.method == "POST":
        city_name = request.form["city_name"]
        api_id = "24034c2fc253da6475cd74bc0b96cf5a"
        api_link = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&APPID={api_id}"

        dict_with_weather_info = requests.get(api_link).json()
        add_flag = True
        city = dict_with_weather_info["name"]
        temperature = int(dict_with_weather_info["main"]["temp"]) - 273
        state = dict_with_weather_info["weather"][0]["main"]
        return render_template("index.html",  add_flag=add_flag, state=state, city=city, temperature=temperature)





# don't change the following way to run flask:
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
