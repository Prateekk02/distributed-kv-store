from fastapi.testclient import TestClient
from app.main import app, store

client = TestClient(app)

### GET missing key test case ###
def test_get_missing_key():
    response = client.get("/kv/nonexistent")
    assert response.status_code == 404
    assert response.json()['detail'] == "Key not found in the database"
   
### PUT missing key test case ###    
def test_put_missing_key():
    response = client.put("/kv/mykey", params={"value": "myvalue"})
    assert response.status_code == 404
    assert response.json()['detail'] == "Key not found in the database"

### DELETE missing key test case ###  
def test_delete_missing_key():
    store.clear()
    response = client.delete("/kv/nonexistent")
    assert response.status_code == 404
    assert response.json()['detail'] == "Key not found in the database"
    
### KV Operations
def test_kv_operations():
    store.clear()
    
    store['testkey'] = 'initial'
    
    # GET 
    response = client.get("/kv/testkey")
    assert response.status_code == 200
    assert response.json() == {"value": "initial"}
    
    # PUT (update)
    response = client.put("/kv/testkey", params={"value": "updated"})
    assert response.status_code == 200
    assert response.json()['message'] == "Key value updated successfully" 
    
    # Confirming update via get
    response = client.get("kv/testkey")
    assert response.status_code == 200
    assert response.json() == {"value" : "updated"}
    
    # DELETE
    response = client.delete("kv/testkey")
    assert response.status_code == 200
    assert response.json()['message'] == "Key deleted successfully"
    
    # Confirming Delete
    response = client.get("kv/testkey")
    assert response.status_code == 404