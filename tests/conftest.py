import pytest
import os
from app.database import create_kv_table, get_connection

@pytest.fixture(scope="session", autouse=True)
def set_test_db_env():
    os.environ["DB_NAME"] = "kvdb_test"      # Use your test DB name
    os.environ["DB_USER"] = "kvuser"
    os.environ["DB_PASSWORD"] = "kvpass"
    os.environ["DB_HOST"] = "localhost"
    os.environ["DB_PORT"] = "5432"

@pytest.fixture(autouse=True)
def clear_table():
    """Ensure table exists and clear database table before every test."""
    create_kv_table()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM kv_store;")
    conn.commit()
    cur.close()
    conn.close()
