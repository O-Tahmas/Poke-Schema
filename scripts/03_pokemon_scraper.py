import requests
from utilities import connect_db, fetch_all, scrape_generations

def get_version_group_mapping():
    version_groups_url = "https://pokeapi.co/api/v2/version-group/"
    version_groups = fetch_all(version_groups_url)
    version_to_generation = {}
    for version_group in version_groups:
        version_data = requests.get(version_group['url']).json()
        generation_id = int(version_data['generation']['url'].split('/')[-2])
        for version in version_data['versions']:
            version_id = int(version['url'].split('/')[-2])
            version_to_generation[version_id] = generation_id
    return version_to_generation

def get_pokemon_data(pokemon_api_result, version_to_generation , generation_matrix):
    
    # Helper function to map a pkmn to a generation based on dex (or id)
    # for those that don't have game indicies
    def get_generation_id_matrix(pokemon_id, generation_matrix):
        for i in range(len(generation_matrix) - 1):
            if generation_matrix[i][1] <= pokemon_id < generation_matrix[i + 1][1]:
                return generation_matrix[i][0]
        return generation_matrix[-1][0]  # If it's the last generation
    
    response = requests.get(pokemon_api_result["url"])
    response_json = response.json()
    pokemon_id = response_json["id"]
    name = response_json["name"]
    height = response_json["height"]
    mass = response_json["weight"]
    base_experience = response_json["base_experience"]
    types = [
        int(type_info["type"]["url"].split("/")[-2])
        for type_info in response_json["types"]
    ]
    type1_id = types[0]
    type2_id = types[1] if len(types) > 1 else None
    try:
        game_index = response_json['game_indices'][0]['version']['url'].split('/')[-2]
        generation_id = version_to_generation[int(game_index)]
    except IndexError:
        generation_id = get_generation_id_matrix(pokemon_id, generation_matrix)
    stats = [
        (
            int(stat_info["stat"]["url"].split("/")[-2]),
            stat_info["base_stat"],
            stat_info["stat"]["name"],
        )
        for stat_info in response_json["stats"]
    ]
    return pokemon_id, name, type1_id, type2_id, height, mass, base_experience, generation_id, stats

def insert_pokemon_data(
    conn, pokemon_id, name, type1_id, type2_id, height, mass, base_experience, generation_id
):
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO pokemon (pokemon_id, pokemon_name, type1_id, type2_id, height, mass, base_experience, generation_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (pokemon_id) DO NOTHING
    """,
        (pokemon_id, name, type1_id, type2_id, height, mass, base_experience, generation_id),
    )
    conn.commit()
    cur.close()


def insert_base_stat(conn, stat_id, stat_name):
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO base_stats (stat_id, stat_name)
        VALUES (%s, %s)
        ON CONFLICT (stat_id) DO NOTHING
    """,
        (stat_id, stat_name),
    )
    conn.commit()
    cur.close()


def insert_pokemon_base_stats(conn, pokemon_id, stats):
    cur = conn.cursor()
    for stat_id, stat_value, stat_name in stats:
        insert_base_stat(conn, stat_id, stat_name)
        cur.execute(
            """
            INSERT INTO pokemon_base_stats (pokemon_id, stat_id, stat_value)
            VALUES (%s, %s, %s)
            ON CONFLICT (pokemon_id, stat_id) DO NOTHING
        """,
            (pokemon_id, stat_id, stat_value),
        )
    conn.commit()
    cur.close()

## Some entries have flawed generational information, so must be manually adjusted! 
def update_pokemon_generations(conn):
    cur = conn.cursor()

    cur.execute("""
        UPDATE pokemon
        SET generation_id = 8
        WHERE pokemon_id BETWEEN 10158 AND 10246;
    """)

    cur.execute("""
        UPDATE pokemon
        SET generation_id = 7
        WHERE pokemon_id BETWEEN 10091 AND 10157;
    """)

    cur.execute("""
        UPDATE pokemon
        SET generation_id = 6
        WHERE pokemon_id BETWEEN 10025 AND 10090;
    """)

    conn.commit()
    cur.close()


def main():

    # Connect to local db
    conn = connect_db()

    # Fetch genarational data
    generation_matrix = scrape_generations()
    version_to_generation = get_version_group_mapping()

    # Fetch pokemon data and split into pokemon table and stat table
    pokemon_url = "https://pokeapi.co/api/v2/pokemon/"
    all_pokemon = fetch_all(pokemon_url)
    for pokemon_api_result in all_pokemon:
        pokemon_id, name, type1_id, type2_id, height, mass, base_experience, generation_id, stats = (
            get_pokemon_data(pokemon_api_result, version_to_generation, generation_matrix)
        )
        insert_pokemon_data(
            conn, pokemon_id, name, type1_id, type2_id, height, mass, base_experience, generation_id
        )
        insert_pokemon_base_stats(conn, pokemon_id, stats)
    
    # To cover for the flawed generational data
    update_pokemon_generations(conn)

    # Close connection
    conn.close()

if __name__ == "__main__":
    main()

