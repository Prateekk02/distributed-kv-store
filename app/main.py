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

def get_db():
    conn = get_connection()
    cur = conn.cursor()
    try:
        yield cur
        conn.commit()
    finally:
        cur.close()
        conn.close()
        
        
app = FastAPI(lifespan=lifespan)

@app.put("/kv/{key}")
def put_key(key:str, value:str, cur = Depends(get_db)):
    cur.execute("INSERT INTO kv_store (key, value) VALUES (%s, %s) ON CONFLICT (key) DO UPDATE SET VALUE = EXCLUDED.value;", (key, value))
    return {"message": "Key stored"}
   
        
@app.get("/kv/{key}")
def get_key(key:str, cur = Depends(get_db)):   
    cur.execute("SELECT value FROM kv_store WHERE key = %s;", (key,))
    row = cur.fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Key not found")        
    return {"value", row[0]}
    
        
@app.delete("/kv/{key}")
def delete_key(key:str, cur = Depends(get_db)):   
    cur.execute("DELETE FROM kv_store WHERE key = %s;", (key,))
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Key not found")    
    return {"message": "Key deleted successfully"}
   