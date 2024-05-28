import pytest
from scripts.utilities import connect_db

def test_db_connection():
    conn = connect_db()
    assert conn is not None
    conn.close()
