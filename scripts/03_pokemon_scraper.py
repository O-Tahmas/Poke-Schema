import requests
from local_db import connect_db


def fetch_all_pokemon():
    url = "https://pokeapi.co/api/v2/pokemon/"
    pokemon = []
    while url:
        response = requests.get(url)
        data = response.json()
        pokemon.extend(data['results'])
        url = data['next']
        break
    return pokemon


def main():
    all_pokemon = fetch_all_pokemon()
    print(len(all_pokemon))