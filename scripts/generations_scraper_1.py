import requests
from utilities import connect_db, fetch_all


def get_generation_data(generation_api_result):
    response = requests.get(generation_api_result["url"])
    response_json = response.json()
    generation_id = response_json["id"]
    generation_name = response_json["name"]
    return generation_id, generation_name


def insert_generation_data(conn, generation_id, generation_name):
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO generations (generation_id, generation_name)
        VALUES (%s, %s)
        ON CONFLICT (generation_id) DO NOTHING
    """,
        (generation_id, generation_name),
    )
    conn.commit()
    cur.close()


def get_region_data(region_api_result):
    response = requests.get(region_api_result["url"])
    response_json = response.json()
    region_id = response_json["id"]
    region_name = response_json["name"]
    if not response_json["main_generation"] and region_id == 9:
        generation_id = 8 #  hisui is not accounted for on pokeapi
    else:
        generation_id = int(response_json["main_generation"]["url"].split("/")[-2])
    return region_id, region_name, generation_id


def insert_region_data(conn, region_id, region_name, gen_id):
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO regions (region_id, region_name, generation_id)
        VALUES (%s, %s, %s)
        ON CONFLICT (region_id) DO NOTHING
    """,
        (region_id, region_name, gen_id),
    )
    conn.commit()
    cur.close()


def get_location_data(location_api_result):
    response = requests.get(location_api_result["url"])
    response_json = response.json()
    location_id = response_json["id"]
    location_name = response_json["name"]
    region_id = (
        int(response_json["region"]["url"].split("/")[-2])
        if response_json["region"]
        else None
    )
    return location_id, location_name, region_id


def insert_location_data(conn, location_id, location_name, region_id):
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO locations (location_id, location_name, region_id)
        VALUES (%s, %s, %s)
        ON CONFLICT (location_id) DO NOTHING
    """,
        (location_id, location_name, region_id),
    )
    conn.commit()
    cur.close()


def fetch_locations():
    url = "https://pokeapi.co/api/v2/location/"
    response = requests.get(url)
    return response.json()["results"]


def get_location_data(location_api_result):
    response = requests.get(location_api_result["url"])
    response_json = response.json()
    location_id = response_json["id"]
    location_name = response_json["name"]
    region_id = (
        int(response_json["region"]["url"].split("/")[-2])
        if response_json["region"]
        else None
    )
    return location_id, location_name, region_id


def insert_location_data(conn, location_id, location_name, region_id):
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO locations (location_id, location_name, region_id)
        VALUES (%s, %s, %s)
        ON CONFLICT (location_id) DO NOTHING
    """,
        (location_id, location_name, region_id),
    )
    conn.commit()
    cur.close()


def get_version_group_data(version_group_api_result):
    response = requests.get(version_group_api_result["url"])
    response_json = response.json()
    version_id = response_json["id"]
    version_name = response_json["name"]
    generation_id = (
        int(response_json["generation"]["url"].split("/")[-2])
        if response_json["generation"]
        else None
    )
    return version_id, version_name, generation_id


def insert_version_group_data(conn, version_id, version_name, generation_id):
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO game_versions (version_id, version_name, generation_id)
        VALUES (%s, %s, %s)
        ON CONFLICT (version_id) DO NOTHING
    """,
        (version_id, version_name, generation_id),
    )
    conn.commit()
    cur.close()


def get_game_data(game_api_result):
    response = requests.get(game_api_result["url"])
    response_json = response.json()
    game_id = response_json["id"]
    game_name = response_json["name"]
    version_id = (
        int(response_json["version_group"]["url"].split("/")[-2])
        if response_json["version_group"]
        else None
    )
    return game_id, game_name, version_id


def insert_game_data(conn, game_id, game_name, version_id):
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO games (game_id, game_name, version_id)
        VALUES (%s, %s, %s)
        ON CONFLICT (game_id) DO NOTHING
    """,
        (game_id, game_name, version_id),
    )
    conn.commit()
    cur.close()


def main():

    # Connect to local db
    conn = connect_db()

    # Populate Generations
    generations_url = "https://pokeapi.co/api/v2/generation/"
    generations = fetch_all(generations_url)
    for generation_api_result in generations:
        generation_id, generation_name = get_generation_data(generation_api_result)
        insert_generation_data(conn, generation_id, generation_name)

    # Populate Regions
    regions_url = "https://pokeapi.co/api/v2/region/"
    regions = fetch_all(regions_url)
    for region_api_result in regions:
        region_id, region_name, gen_id = get_region_data(region_api_result)
        insert_region_data(conn, region_id, region_name, gen_id)

    # Populate Locations
    locations_url = "https://pokeapi.co/api/v2/location/"
    locations = fetch_all(locations_url)
    for location_api_result in locations:
        location_id, location_name, region_id = get_location_data(location_api_result)
        if location_id != 1045:  ## duplicate of malie-city! Have opened a PR on pokeapi
            insert_location_data(conn, location_id, location_name, region_id)

    # Populate Game Versions
    version_groups_url = "https://pokeapi.co/api/v2/version-group/"
    version_groups = fetch_all(version_groups_url)
    for version_group_api_result in version_groups:
        version_id, version_name, generation_id = get_version_group_data(
            version_group_api_result
        )
        insert_version_group_data(conn, version_id, version_name, generation_id)

    # Populate Games
    games_url = "https://pokeapi.co/api/v2/version/"
    games = fetch_all(games_url)
    for game_api_result in games:
        game_id, game_name, version_id = get_game_data(game_api_result)
        insert_game_data(conn, game_id, game_name, version_id)

    # Close connection
    conn.close()


if __name__ == "__main__":
    main()
