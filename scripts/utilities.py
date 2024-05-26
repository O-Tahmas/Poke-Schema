import psycopg2
import requests


def connect_db():
    conn = psycopg2.connect(
        dbname="pokemon_db",
        user="postgres",  # default values, change as per local config
        password="admin",  # default values, change as per local config
        host="localhost",
    )
    return conn


def fetch_all(url):
    data_out = []
    while url:
        response = requests.get(url)
        data = response.json()
        data_out.extend(data["results"])
        url = data["next"]
    return data_out
