import os

SQLALCHEMY_DATABASE_URI = 'sqlite:///weather.db'
key = os.urandom(24)
SECRET_KEY = key
