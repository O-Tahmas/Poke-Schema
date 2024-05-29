import pytest
import yaml
import psycopg2
import requests
from bs4 import BeautifulSoup
from unittest.mock import patch, mock_open
from scripts.utilities import load_config, connect_db, fetch_all, scrape_generations

# Test for load_config function
def test_load_config():
    mock_config = """
    database:
      dbname: "pokemon_db"
      user: "postgres"
      password: "admin"
      host: "localhost"
      port: 5432
    """
    
    with patch("builtins.open", mock_open(read_data=mock_config)):
        config = load_config()
        assert config["database"]["dbname"] == "pokemon_db"
        assert config["database"]["user"] == "postgres"
        assert config["database"]["password"] == "admin"
        assert config["database"]["host"] == "localhost"
        assert config["database"]["port"] == 5432

# Test for connect_db function
@patch("scripts.utilities.load_config")
@patch("psycopg2.connect")
def test_connect_db(mock_connect, mock_load_config):
    # Mocking the load_config function to return a specific configuration
    mock_load_config.return_value = {
        "database": {
            "dbname": "pokemon_db",
            "user": "postgres",
            "password": "admin",
            "host": "localhost",
            "port": 5432
        }
    }
    
    # Call the connect_db function, which should use the mocked configuration
    conn = connect_db()
    
    # Verify that psycopg2.connect was called with the expected parameters
    mock_connect.assert_called_once_with(
        dbname="pokemon_db",
        user="postgres",
        password="admin",
        host="localhost",
        port=5432
    )
    
    # Ensure the connection object returned is the mock connection
    assert conn == mock_connect.return_value

# Test for fetch_all function
@patch("requests.get")
def test_fetch_all(mock_get):
    mock_response = mock_get.return_value
    mock_response.json.return_value = {
        "results": [{"name": "bulbasaur"}, {"name": "ivysaur"}],
        "next": None
    }
    
    url = "https://pokeapi.co/api/v2/pokemon/"
    data = fetch_all(url)
    assert len(data) == 2
    assert data[0]["name"] == "bulbasaur"
    assert data[1]["name"] == "ivysaur"

# Test for scrape_generations function
@patch("requests.get")
def test_scrape_generations(mock_get):
    mock_html = """
    <div class="infocard-list infocard-list-pkmn-lg">
        <div>
            <small>#001</small>
        </div>
    </div>
    <div class="infocard-list infocard-list-pkmn-lg">
        <div>
            <small>#152</small>
        </div>
    </div>
    """
    mock_response = mock_get.return_value
    mock_response.content = mock_html
    
    generation_matrix = scrape_generations()
    assert len(generation_matrix) == 2
    assert generation_matrix[0] == [1, 1]
    assert generation_matrix[1] == [2, 152]

# Running all tests together
if __name__ == "__main__":
    pytest.main()
