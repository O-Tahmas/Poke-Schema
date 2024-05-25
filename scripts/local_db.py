import psycopg2

def connect_db():
    conn = psycopg2.connect(
        dbname="pokemon_db",
        user="postgres",  # default values, change as per local config
        password="admin",  # default values, change as per local config
        host="localhost"
    )
    return conn
