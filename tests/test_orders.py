import httpx

BASE_URL = "http://localhost:8000"

def get_token():
    response = httpx.post(
        f"{BASE_URL}/auth/login",
        json={"email": "admin@example.com", "password": "admin123"}
    )
    return response.json()["access_token"]

def test_loan_and_return():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    # LOAN BOOK_ID = 1
    loan = httpx.post(f"{BASE_URL}/orders/loan/1", headers=headers)
    assert loan.status_code == 200
    order = loan.json()
    order_id = order["order_id"]

    assert order["return_date"] is None

    # RETURN BOOK
    ret = httpx.post(f"{BASE_URL}/orders/return/{order_id}", headers=headers)
    assert ret.status_code == 200
    assert ret.json()["return_date"] is not None
