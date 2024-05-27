import psycopg2
import requests
from bs4 import BeautifulSoup


def connect_db():
    conn = psycopg2.connect(
        dbname="pokemon_db",
        user="postgres",  # default values, change as per local config
        password="admin",  # default values, change as per local config
        host="localhost",
    )
    return conn

# Stop trying to make `fetch` happen, it's not going to happen!
def fetch_all(url):
    data_out = []
    while url:
        response = requests.get(url)
        data = response.json()
        data_out.extend(data["results"])
        url = data["next"]
        # break # helpful when wanting to test an initial sample
    return data_out

# bs4 scraper to pull mappings of national dex #'s to generations
def scrape_generations():
    def convert_hashed_number(s):
        num = s.replace('#', '')
        num_out = ''
        num_hit = False
        for char in num:
            if char == '0' and num_hit is False:
                continue
            else:
                num_hit = True
                num_out +=char
        return int(num_out)
    url = "https://pokemondb.net/pokedex/national/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    generation_matrix = []
    generation_markers = soup.find_all('div', class_='infocard-list infocard-list-pkmn-lg')
    gen = 1
    for generation_mark in generation_markers:
        first_pkmn = generation_mark.find('div')
        pokemon_idx = first_pkmn.find('small').text
        generation_matrix.append([int(gen), convert_hashed_number(pokemon_idx)])
        gen +=1
    return generation_matrix
