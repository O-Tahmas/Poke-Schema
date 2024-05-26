import requests
from utilities import connect_db, fetch_all


def fetch_pokemon_types_():
    url = "https://pokeapi.co/api/v2/type/"
    types = []
    while url:
        response = requests.get(url)
        data = response.json()
        types.extend(data["results"])
        url = data["next"]  # Get the next URL, if available
    return types


# Get type data from the API result
def get_type_data(type_api_result):
    response = requests.get(type_api_result["url"])
    response_json = response.json()
    type_id = response_json["id"]
    name = response_json["name"]
    generation = response_json["generation"]["url"].split("/")[-2]
    damage_relations = []
    for relation, related_types in response_json["damage_relations"].items():
        multiplier = {
            "no_damage_to": 0.0,
            "half_damage_to": 0.5,
            "double_damage_to": 2.0,
            "no_damage_from": 0.0,
            "half_damage_from": 0.5,
            "double_damage_from": 2.0,
        }[relation]
        for related_type in related_types:
            related_type_id = int(related_type["url"].split("/")[-2])
            damage_relations.append((type_id, related_type_id, multiplier))
    return [type_id, name, generation, damage_relations]


# Insert type data into the database
def insert_type_data(conn, type_id, name, generation):
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO pkmn_types (type_id, type_name, generation)
        VALUES (%s, %s, %s)
        ON CONFLICT (type_id) DO NOTHING
    """,
        (type_id, name, generation),
    )
    conn.commit()
    cur.close()


# Insert damage relations into the database
# Only relations that are <> 1 are inserted, to save space
def insert_damage_relations(conn, damage_relations):
    cur = conn.cursor()
    for type_id, related_type_id, multiplier in damage_relations:
        cur.execute(
            """
            INSERT INTO type_relations (type_id, related_type_id, dmg_multiplier)
            VALUES (%s, %s, %s)
            ON CONFLICT (type_id, related_type_id) DO NOTHING
        """,
            (type_id, related_type_id, multiplier),
        )
    conn.commit()
    cur.close()


def main():

    # Connect to local db
    conn = connect_db()

    # Fetch and insert types and relations
    type_url = "https://pokeapi.co/api/v2/type/"
    pokemon_types = fetch_all(type_url)

    # Need to loop through twice, so that PostGres allows for foriegn insertions properly
    type_entries = [get_type_data(type_api_result) for type_api_result in pokemon_types]
    for entry in type_entries:
        type_id, name, generation = entry[0], entry[1], entry[2]
        insert_type_data(conn, type_id, name, generation)
    for entry in type_entries:
        damage_relations = entry[3]
        insert_damage_relations(conn, damage_relations)

    # Close connection
    conn.close()
