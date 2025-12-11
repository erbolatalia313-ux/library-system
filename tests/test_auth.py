import httpx

BASE_URL = "http://localhost:8000"

def test_login_success():
    response = httpx.post(
        f"{BASE_URL}/auth/login",
        json={"email": "admin@example.com", "password": "admin123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
