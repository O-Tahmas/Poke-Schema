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

def get_pokemon_data(pokemon_api_result):
    response = requests.get(pokemon_api_result['url'])
    response_json = response.json()
    pokemon_id = response_json['id']
    name = response_json['name']
    height = response_json['height']
    mass = response_json['weight']
    base_experience = response_json['base_experience']
    types = [int(type_info['type']['url'].split('/')[-2]) for type_info in response_json['types']]
    type1_id = types[0]
    type2_id = types[1] if len(types) > 1 else None
    stats = [(int(stat_info['stat']['url'].split('/')[-2]), stat_info['base_stat'], stat_info['stat']['name']) for stat_info in response_json['stats']]
    return pokemon_id, name, type1_id, type2_id, height, mass, base_experience, stats

def insert_pokemon_data(conn, pokemon_id, name, type1_id, type2_id, height, mass, base_experience):
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO pokemon (pokemon_id, pokemon_name, type1_id, type2_id, height, mass, base_experience)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (pokemon_id) DO NOTHING
    """, (pokemon_id, name, type1_id, type2_id, height, mass, base_experience))
    conn.commit()
    cur.close()

def insert_base_stat(conn, stat_id, stat_name):
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO base_stats (stat_id, stat_name)
        VALUES (%s, %s)
        ON CONFLICT (stat_id) DO NOTHING
    """, (stat_id, stat_name))
    conn.commit()
    cur.close()

def insert_pokemon_base_stats(conn, pokemon_id, stats):
    cur = conn.cursor()
    for stat_id, stat_value, stat_name in stats:
        insert_base_stat(conn, stat_id, stat_name)
        cur.execute("""
            INSERT INTO pokemon_base_stats (pokemon_id, stat_id, stat_value)
            VALUES (%s, %s, %s)
            ON CONFLICT (pokemon_id, stat_id) DO NOTHING
        """, (pokemon_id, stat_id, stat_value))
    conn.commit()
    cur.close()

def main():
    conn = connect_db()
    all_pokemon = fetch_all_pokemon()
    
    for pokemon_api_result in all_pokemon:
        pokemon_id, name, type1_id, type2_id, height, mass, base_experience, stats = get_pokemon_data(pokemon_api_result)
        insert_pokemon_data(conn, pokemon_id, name, type1_id, type2_id, height, mass, base_experience)
        insert_pokemon_base_stats(conn, pokemon_id, stats)
    
    conn.close()

if __name__ == "__main__":
    main()
