from fastapi import FastAPI, HTTPException, Depends
from .database import get_connection, create_kv_table
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    get_connection()
    print("Connected to database")
    create_kv_table()
    print("Created kv table")
    yield
    print("Shutting down app")


app = FastAPI(lifespan=lifespan)

@app.put("/kv/{key}")
def put_key(key:str, value:str):
    conn = get_connection()
    cur = conn.cursor()
         
    try:
        cur.execute("INSERT INTO kv_store (key, value) VALUES (%s, %s) ON CONFLICT (key) DO UPDATE SET VALUE = EXCLUDED.value;", (key, value))
        conn.commit()
        return {"message": "Key stored"}
    finally: 
        cur.close()
        conn.close()
        
@app.get("/kv/{key}")
def get_key(key:str):
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("SELECT value FROM kv_store WHERE key = %s;", (key,))
        row = cur.fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Key not found")
        
        return {"value", row[0]}
    finally:
        cur.close()
        conn.close()
        
@app.delete("/kv/{key}")
def delete_key(key:str):
    conn = get_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("DELETE FROM kv_store WHERE key = %s;", (key,))
        if cur.rowcount == 0:
            raise HTTPException(status_code=404, detail="Key not found")
        conn.commit()
        return {"message": "Key deleted successfully"}
    finally:
        cur.close()
        conn.close()