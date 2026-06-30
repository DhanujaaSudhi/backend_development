# Stage 7: Testing

## Objective
Implement comprehensive testing for the FastAPI application using playwright and pytest to ensure API reliability and catch bugs early.

## Acceptance Criteria
- Tests cover all CRUD operations
- Tests verify error handling
- Tests validate response formats
- All tests pass successfully

## Implementation

### Test Setup

**Install Dependencies:**
```bash
pip install pytest httpx
```

**Test File Structure:**
```python
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)
```

### Test Examples

**Create Hero Test:**
```python
def test_create_hero():
    response = client.post(
        "/heroes/",
        json={"name": "Test Hero", "secret_name": "Secret Identity", "age": 25}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Hero"
    assert "id" in data
```

**Validation Error Test:**
```python
def test_create_hero_validation_error():
    response = client.post(
        "/heroes/",
        json={"name": "Test Hero"}
    )
    assert response.status_code == 422
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
```

**Read Hero Test:**
```python
def test_read_hero():
    create_response = client.post(
        "/heroes/",
        json={"name": "Read Test Hero", "secret_name": "Secret", "age": 30}
    )
    hero_id = create_response.json()["id"]
    
    response = client.get(f"/heroes/{hero_id}")
    assert response.status_code == 200
    assert response.json()["id"] == hero_id
```

**Not Found Error Test:**
```python
def test_read_hero_not_found():
    response = client.get("/heroes/99999")
    assert response.status_code == 404
    data = response.json()
    assert data["error"]["code"] == "HTTP_ERROR"
```

**Update Hero Test:**
```python
def test_update_hero():
    create_response = client.post(
        "/heroes/",
        json={"name": "Update Test Hero", "secret_name": "Secret", "age": 25}
    )
    hero_id = create_response.json()["id"]
    
    response = client.patch(
        f"/heroes/{hero_id}",
        json={"name": "Updated Hero Name", "age": 26}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Hero Name"
```

**Delete Hero Test:**
```python
def test_delete_hero():
    create_response = client.post(
        "/heroes/",
        json={"name": "Delete Test Hero", "secret_name": "Secret", "age": 25}
    )
    hero_id = create_response.json()["id"]
    
    response = client.delete(f"/heroes/{hero_id}")
    assert response.status_code == 200
    assert response.json()["ok"] is True
```

**Error Response Format Test:**
```python
def test_error_response_format():
    response = client.get("/heroes/99999")
    assert response.status_code == 404
    data = response.json()
    
    assert "error" in data
    assert "meta" in data
    assert "code" in data["error"]
    assert "message" in data["error"]
```

### Running Tests

**Run all tests:**
```bash
pytest
```

**Run with verbose output:**
```bash
pytest -v
```

**Run specific test file:**
```bash
pytest test_main.py
```

## Test Results

All 12 tests passed successfully:
- ✅ test_create_hero
- ✅ test_create_hero_validation_error
- ✅ test_read_hero
- ✅ test_read_hero_not_found
- ✅ test_read_heroes
- ✅ test_read_heroes_with_pagination
- ✅ test_update_hero
- ✅ test_update_hero_not_found
- ✅ test_delete_hero
- ✅ test_delete_hero_not_found
- ✅ test_error_response_format
- ✅ test_validation_error_format

## Benefits

**Testing:**
- Catches bugs before production
- Ensures API reliability
- Documents expected behavior
- Enables safe refactoring
- Provides regression protection

**TestClient:**
- No need to run server
- Fast test execution
- Easy to use (similar to httpx/requests)
- Integrates with pytest
- Supports all HTTP methods

## Best Practices

- Test both success and error cases
- Test validation errors
- Verify response formats
- Use descriptive test names
- Keep tests independent
- Test edge cases
- Mock external dependencies when needed
