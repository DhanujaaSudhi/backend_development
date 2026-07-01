from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_verify_employee_success():
    response = client.post("/api/v1/auth/verify-employee", json={
        "employee_id": "EMP100",
        "verification_method": "email"
    })
    assert response.status_code == 200
    assert "OTP sent successfully" in response.json()["data"]["message"]

def test_verify_employee_invalid():
    response = client.post("/api/v1/auth/verify-employee", json={
        "employee_id": "INVALID",
        "verification_method": "email"
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "Information does not match our records"

def test_verify_otp_success():
    response = client.post("/api/v1/auth/verify-otp", json={
        "employee_id": "EMP100",
        "otp": "12345"
    })
    assert response.status_code == 200

def test_verify_otp_invalid_format():
    response = client.post("/api/v1/auth/verify-otp", json={
        "employee_id": "EMP100",
        "otp": "12" # Too short, fails Pydantic schema validation (Stage 4)
    })
    assert response.status_code == 422 # Pydantic validation error
