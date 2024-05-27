import requests
from utilities import connect_db, fetch_all

def insert_move_auxiliary_data(conn, table_name, data):
    cur = conn.cursor()
    for item in data:
        item_id = item["url"].split("/")[-2]
        item_name = item['name']
        cur.execute(f"""
            INSERT INTO {table_name} (id, name)
            VALUES (%s, %s)
            ON CONFLICT (id) DO NOTHING
        """, (item_id, item_name))
    conn.commit()
    cur.close()



def get_move_data(move_api_result):
    response = requests.get(move_api_result['url'])
    response_json = response.json()

    move_id = response_json['id']
    name = response_json['name']
    type_id = int(response_json['type']['url'].split('/')[-2]) if response_json['type'] else None
    priority_rank = response_json.get('priority', None)
    power = response_json.get('power', None)
    accuracy = response_json.get('accuracy', None)
    effect_chance = response_json.get('effect_chance', None)
    pp = response_json.get('pp', None)

    meta = response_json.get('meta', None)
    crit_rate = meta.get('crit_rate', None) if meta else None
    drain = meta.get('drain', None) if meta else None
    flinch_chance = meta.get('flinch_chance', None) if meta else None
    healing = meta.get('healing', None) if meta else None
    max_hits = meta.get('max_hits', None) if meta else None
    max_turns = meta.get('max_turns', None) if meta else None
    min_hits = meta.get('min_hits', None) if meta else None
    min_turns = meta.get('min_turns', None) if meta else None
    stat_chance = meta.get('stat_chance', None) if meta else None
    damage_class_id = int(response_json['damage_class']['url'].split('/')[-2]) if response_json['damage_class'] else None
    ailment_id = int(meta['ailment']['url'].split('/')[-2]) if meta and 'ailment' in meta else None
    category_id = int(meta['category']['url'].split('/')[-2]) if meta and 'category' in meta else None
    generation_id = int(response_json['generation']['url'].split('/')[-2]) if response_json['generation'] else None
    target_id = int(response_json['target']['url'].split('/')[-2]) if response_json['target'] else None

    # Get learned_by_pokemon data
    learned_by_pokemon = [
        int(pokemon['url'].split('/')[-2])
        for pokemon in response_json['learned_by_pokemon']
    ]

    # Get stat changes data
    stat_changes = [
        (int(change['stat']['url'].split('/')[-2]), change['change'])
        for change in response_json.get('stat_changes', [])
    ]

    return (
        move_id, name, type_id, priority_rank, power, accuracy, effect_chance,
        pp, crit_rate, drain, flinch_chance, healing, max_hits, max_turns,
        min_hits, min_turns, stat_chance, damage_class_id, ailment_id,
        category_id, generation_id, target_id, learned_by_pokemon, stat_changes
    )


def insert_move_data(conn, move_data):
    cur = conn.cursor()
    (
        move_id, name, type_id, priority_rank, power, accuracy, effect_chance,
        pp, crit_rate, drain, flinch_chance, healing, max_hits, max_turns,
        min_hits, min_turns, stat_chance, damage_class_id, ailment_id,
        category_id, generation_id, target_id, learned_by_pokemon, stat_changes
    ) = move_data

    cur.execute("""
        INSERT INTO moves (
            move_id, move_name, type_id, priority_rank, power, accuracy, effect_chance, pp,
            crit_rate, drain, flinch_chance, healing, max_hits, max_turns, min_hits, min_turns,
            stat_chance, damage_class_id, ailment_id, category_id, generation_id, target_id
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (move_id) DO NOTHING
    """, (
        move_id, name, type_id, priority_rank, power, accuracy, effect_chance,
        pp, crit_rate, drain, flinch_chance, healing, max_hits, max_turns,
        min_hits, min_turns, stat_chance, damage_class_id, ailment_id,
        category_id, generation_id, target_id
    ))

    # Insert learned_by_pokemon data
    for pokemon_id in learned_by_pokemon:
        cur.execute("""
            INSERT INTO pokemon_movesets (learned_by_pokemon, move_id)
            VALUES (%s, %s)
            ON CONFLICT (learned_by_pokemon, move_id) DO NOTHING
        """, (pokemon_id, move_id))

    # Insert stat_changes data
    for stat_id, change in stat_changes:
        cur.execute("""
            INSERT INTO move_stat_changes (move_id, stat_id, change)
            VALUES (%s, %s, %s)
            ON CONFLICT (move_id, stat_id) DO NOTHING
        """, (move_id, stat_id, change))

    conn.commit()
    cur.close()

def main():

    # Connect to local db
    conn = connect_db()

    # Use the auxillary table function to easily populate the lightweight move 'subject' tables
    move_subject_urls = ["https://pokeapi.co/api/v2/move-category/","https://pokeapi.co/api/v2/move-damage-class/",
                         "https://pokeapi.co/api/v2/move-ailment/", "https://pokeapi.co/api/v2/move-target/"]
    table_names = ['move_categories', 'move_damage_classes', 'move_ailments', 'move_targets']
    for i in range(len(table_names)):
        fetched = fetch_all(move_subject_urls[i])
        insert_move_auxiliary_data(conn, table_names[i], fetched)
    
    # Fetch move data
    moves_url = "https://pokeapi.co/api/v2/move/"
    all_moves = fetch_all(moves_url)
    for move_api_result in all_moves:
        move_data = get_move_data(move_api_result)
        insert_move_data(conn, move_data)

    # Close connection
    conn.close()

if __name__ == "__main__":
    main()
