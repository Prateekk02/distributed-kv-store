from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app=app)

def test_put_and_get_key():
    key = "test_key"
    value = "test_value"
    
    # PUT request
    response = client.put(f"/kv/{key}",params={"value":value})
    assert response.status_code == 200
    assert response.json() == {"message": "Key stored"}
    
    # GET request
    response = client.get(f"/kv/{key}")
    assert response.status_code==200
    assert response.json() == {"value": value}
    

def test_get_nonexistent_key():
    response = client.get("/kv/nonexistent")
    assert response.status_code == 404
    assert response.json()['detail'] == 'Key not found' 
    

def test_delete_key():
    key = "keytodelete"
    value = "somevalue"
    
    # Insert first
    response = client.put(f"/kv/{key}", params={"value": value})
    assert response.status_code == 200
    assert response.json()["message"] == "Key stored"
    
    # Delete 
    response = client.delete(f"/kv/{key}")
    assert response.status_code == 200
    assert response.json()["message"] == "Key deleted successfully"
    
    # Get
    response = client.get(f"/kv/{key}")
    assert response.status_code == 404  
    
def test_delete_nonexistent_key():
    response = client.delete("/kv/ghostkey")
    assert response.status_code == 404
    assert response.json()['detail'] == 'Key not found' 