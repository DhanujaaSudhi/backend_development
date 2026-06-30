from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_create_hero():
    """Test creating a new hero"""
    response = client.post(
        "/heroes/",
        json={"name": "Test Hero", "secret_name": "Secret Identity", "age": 25}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Hero"
    assert data["age"] == 25
    assert "id" in data


def test_create_hero_validation_error():
    """Test validation error when required field is missing"""
    response = client.post(
        "/heroes/",
        json={"name": "Test Hero"}
    )
    assert response.status_code == 422
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Invalid input data"


def test_read_hero():
    """Test reading a hero by ID"""
    # First create a hero
    create_response = client.post(
        "/heroes/",
        json={"name": "Read Test Hero", "secret_name": "Secret", "age": 30}
    )
    hero_id = create_response.json()["id"]
    
    # Then read the hero
    response = client.get(f"/heroes/{hero_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == hero_id
    assert data["name"] == "Read Test Hero"


def test_read_hero_not_found():
    """Test 404 error when hero doesn't exist"""
    response = client.get("/heroes/99999")
    assert response.status_code == 404
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "HTTP_ERROR"
    assert data["error"]["message"] == "Hero not found"


def test_read_heroes():
    """Test reading list of heroes"""
    response = client.get("/heroes/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_read_heroes_with_pagination():
    """Test pagination parameters"""
    response = client.get("/heroes/?offset=0&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_update_hero():
    """Test updating a hero"""
    # First create a hero
    create_response = client.post(
        "/heroes/",
        json={"name": "Update Test Hero", "secret_name": "Secret", "age": 25}
    )
    hero_id = create_response.json()["id"]
    
    # Then update the hero
    response = client.patch(
        f"/heroes/{hero_id}",
        json={"name": "Updated Hero Name", "age": 26}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Hero Name"
    assert data["age"] == 26


def test_update_hero_not_found():
    """Test 404 error when updating non-existent hero"""
    response = client.patch(
        "/heroes/99999",
        json={"name": "Updated Name"}
    )
    assert response.status_code == 404
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "HTTP_ERROR"


def test_delete_hero():
    """Test deleting a hero"""
    # First create a hero
    create_response = client.post(
        "/heroes/",
        json={"name": "Delete Test Hero", "secret_name": "Secret", "age": 25}
    )
    hero_id = create_response.json()["id"]
    
    # Then delete the hero
    response = client.delete(f"/heroes/{hero_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["ok"] is True


def test_delete_hero_not_found():
    """Test 404 error when deleting non-existent hero"""
    response = client.delete("/heroes/99999")
    assert response.status_code == 404
    data = response.json()
    assert "error" in data
    assert data["error"]["code"] == "HTTP_ERROR"


def test_error_response_format():
    """Test that error responses follow the standard format"""
    response = client.get("/heroes/99999")
    assert response.status_code == 404
    data = response.json()
    
    # Check error envelope structure
    assert "error" in data
    assert "meta" in data
    
    # Check error structure
    assert "code" in data["error"]
    assert "message" in data["error"]
    
    # Check meta structure
    assert "timestamp" in data["meta"]
    assert "version" in data["meta"]


def test_validation_error_format():
    """Test that validation errors include details"""
    response = client.post(
        "/heroes/",
        json={"name": "Test"}
    )
    assert response.status_code == 422
    data = response.json()
    
    # Check that validation errors include details
    assert "details" in data["error"]
    assert isinstance(data["error"]["details"], list)
