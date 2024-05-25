import requests
from local_db import connect_db


def fetch_all_moves():
    url = "https://pokeapi.co/api/v2/move/"
    moves = []
    while url:
        response = requests.get(url)
        data = response.json()
        moves.extend(data['results'])
        url = data['next']
    return moves

def get_move_data(move_api_result):
    response = requests.get(move_api_result['url'])
    response_json = response.json()
    move_id = response_json['id']
    name = response_json['name']
    type_id = response_json['type']['url'].split('/')[-2]
    power = response_json.get('power', None)
    accuracy = response_json.get('accuracy', None)
    pp = response_json.get('pp', None)
    return move_id, name, type_id, power, accuracy, pp

def insert_move_data(conn, move_id, name, type_id, power, accuracy, pp):
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO moves (move_id, move_name, type_id, power, accuracy, pp)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (move_id) DO NOTHING
    """, (move_id, name, type_id, power, accuracy, pp))
    conn.commit()
    cur.close()

def main():
    # Connect to local db
    conn = connect_db()
    
    moves = fetch_all_moves()
    for move_api_result in moves:
        move_id, name, type_id, power, accuracy, pp = get_move_data(move_api_result)
        insert_move_data(conn, move_id, name, type_id, power, accuracy, pp)
    
    conn.close()