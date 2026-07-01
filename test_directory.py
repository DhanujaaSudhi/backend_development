from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_employees_list():
    response = client.get("/api/v1/employees")
    assert response.status_code == 200
    data = response.json()
    assert "employees" in data["data"]
    assert data["meta"]["total"] == 2
    assert data["meta"]["page"] == 1

def test_get_employee_detail_success():
    response = client.get("/api/v1/employees/EMP100")
    assert response.status_code == 200
    assert response.json()["data"]["employee"]["employee_id"] == "EMP100"

def test_get_employee_detail_not_found():
    response = client.get("/api/v1/employees/INVALID")
    assert response.status_code == 404

def test_update_employee_role_success():
    response = client.patch("/api/v1/employees/EMP100/role", json={"role": "HR"})
    assert response.status_code == 200
    assert "successfully" in response.json()["data"]["message"]

def test_update_employee_role_invalid_role():
    # "InvalidRole" is not in the Literal type definition
    response = client.patch("/api/v1/employees/EMP100/role", json={"role": "InvalidRole"})
    assert response.status_code == 422 # Pydantic validation error
