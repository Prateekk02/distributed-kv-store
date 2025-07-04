import psycopg2
from psycopg2.extensions import connection
import os
import time
from  dotenv import load_dotenv

load_dotenv()


def get_connection(retries:int = 10, delay:int = 2) -> connection:
        db_name = os.getenv("DB_NAME", "kvdb")
        db_user = os.getenv("DB_USER", "kvuser")
        db_password = os.getenv("DB_PASSWORD", "kvpass")
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", 5432)
        
        for attempt in range(retries):
            try:
                conn = psycopg2.connect(                        
                    dbname=db_name,
                    user=db_user,
                    password=db_password,
                    host=db_host,
                    port=db_port
                )
                return conn
            except psycopg2.OperationalError as e:
                print(f"[DB] connection failed (attempt {attempt + 1} / {retries}): {e}")

                time.sleep(delay)
        raise Exception("Could not connect to the database after multiple attempts.")
                
                
    

def create_kv_table():
    conn = get_connection()
    curr = conn.cursor()
    try: 
        curr.execute("""
             CREATE TABLE IF NOT EXISTS kv_store(
                key TEXT PRIMARY KEY,
                value TEXT 
             );        
        """)
        conn.commit()
    finally: 
        curr.close()
        conn.close()