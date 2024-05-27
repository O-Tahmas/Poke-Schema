import requests
from utilities import connect_db, fetch_all

def insert_evolution_triggers(trigger_results, conn):
    cur = conn.cursor()
    for trigger in trigger_results:
        trigger_id = trigger['url'].split('/')[-2]
        trigger_name = trigger['name']
        cur.execute(
            """
            INSERT INTO evolution_triggers (trigger_id, evolution_trigger)
            VALUES (%s, %s)
            ON CONFLICT (trigger_id) DO NOTHING
            """,
            (trigger_id, trigger_name)
        )
    conn.commit()
    cur.close()


def process_evolution_chain(chain, chain_group_id):
    # Helper function to properly extract info from potential metadata formatting 
    def extract_value(data_item, idx):
        if not data_item.get(idx):
            return None
        if type(data_item.get(idx)) is not dict:
            return data_item.get(idx)
        return int(data_item.get(idx).get('url').split('/')[-2])
    
    results = []
    queue = [(chain, 1, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)]  # (current_chain, evolution_order, trigger_id, gender, held_item, item, known_move, known_move_type, location, min_affection, min_beauty, min_happiness, min_level, needs_overworld_rain, party_species, party_type, relative_physical_stats, time_of_day, trade_species)

    while queue:
        current_chain, evolution_order, trigger_id, gender, held_item, item, known_move, known_move_type, location, min_affection, min_beauty, min_happiness, min_level, needs_overworld_rain, party_species, party_type, relative_physical_stats, time_of_day, trade_species = queue.pop(0)
        species_id = int(current_chain['species']['url'].split('/')[-2])
        results.append((chain_group_id, species_id, trigger_id, 
                        evolution_order, gender, held_item, item, known_move, 
                        known_move_type, location, min_affection, min_beauty, 
                        min_happiness, min_level, needs_overworld_rain, party_species, 
                        party_type, relative_physical_stats, time_of_day, trade_species))
        
        for evolves_to in current_chain['evolves_to']:
            for evolution_detail in evolves_to['evolution_details']:
                next_trigger_id = int(evolution_detail['trigger']['url'].split('/')[-2]) if evolution_detail['trigger'] else None
                queue.append((evolves_to, evolution_order + 1, next_trigger_id,
                              extract_value(evolution_detail, 'gender'),
                              extract_value(evolution_detail, 'held_item'),
                              extract_value(evolution_detail, 'item'),
                              extract_value(evolution_detail, 'known_move'),
                              extract_value(evolution_detail, 'known_move_type'),
                              extract_value(evolution_detail, 'location'),
                              extract_value(evolution_detail, 'min_affection'),
                              extract_value(evolution_detail, 'min_beauty'),
                              extract_value(evolution_detail, 'min_happiness'),
                              extract_value(evolution_detail, 'min_level'),
                              0 if not extract_value(evolution_detail, 'needs_overworld_rain') else 1,
                              extract_value(evolution_detail, 'party_species'),
                              extract_value(evolution_detail, 'party_type'),
                              extract_value(evolution_detail, 'relative_physical_stats'),
                              extract_value(evolution_detail, 'time_of_day'),
                              extract_value(evolution_detail, 'trade_species')
                              ))
    return results


def insert_evolution_chains(evolution_chain_data, conn):
    cur = conn.cursor()
    for chain_group_id, pokemon_id, trigger_id, evolution_order, gender, held_item, item, known_move, known_move_type, location, min_affection, min_beauty, min_happiness, min_level, needs_overworld_rain, party_species, party_type, relative_physical_stats, time_of_day, trade_species in evolution_chain_data:
        cur.execute(
            """
            INSERT INTO evolution_chains (chain_group_id, pokemon_id, trigger_id, evolution_order, gender, held_item, item, known_move, known_move_type, location, min_affection, min_beauty, min_happiness, min_level, needs_overworld_rain, party_species, party_type, relative_physical_stats, time_of_day, trade_species)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (chain_group_id, pokemon_id) DO NOTHING
            """,
            (chain_group_id, pokemon_id, trigger_id, evolution_order, gender, held_item, item, known_move, known_move_type, location, min_affection, min_beauty, min_happiness, min_level, needs_overworld_rain, party_species, party_type, relative_physical_stats, time_of_day, trade_species)
        )
    conn.commit()
    cur.close()

def main():
    
    # Connect to local db
    conn = connect_db()

    # Fetch and insert evo-trigger groupings
    url = "https://pokeapi.co/api/v2/evolution-trigger/"
    triggers = fetch_all(url)
    insert_evolution_triggers(triggers, conn)

    # Fetch and insert evolution chains
    url = "https://pokeapi.co/api/v2/evolution-chain/"
    chains = fetch_all(url)
    conn = connect_db()
    for chain in chains:
        response = requests.get(chain['url'])
        chain_json = response.json()
        chain_group_id = chain_json['id']
        chain_data = process_evolution_chain(chain_json['chain'], chain_group_id)
        insert_evolution_chains(chain_data, conn)

    # Close conection
    conn.close()

if __name__ == "__main__":
    main()
