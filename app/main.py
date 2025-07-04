from fastapi import FastAPI, HTTPException

app = FastAPI()
store = {}

@app.get("/kv/{key}")
def get_key(key:str):
    # Check if key is present in the store
    if key not in store:
        raise  HTTPException(status_code=404 , detail="Key not found in the database")     
    return {"value": store[key]}


@app.put("/kv/{key}")
def put_key(key: str, value:str):    
    # Check if key is present in the database
    if key not in store:
        raise HTTPException(status_code=404, detail="Key not found in the database")    
    store[key] = value    
    return {"message": "Key value updated successfully"}  

@app.delete("/kv/{key}")
def delete_key(key:str):
    if key not in store:
        raise HTTPException(status_code=404, detail="Key not found in the database")    
    del store[key]
    return {"message": "Key deleted successfully"}
 