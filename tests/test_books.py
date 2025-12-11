import httpx

BASE_URL = "http://localhost:8000"

def get_token():
    response = httpx.post(
        f"{BASE_URL}/auth/login",
        json={"email": "admin@example.com", "password": "admin123"}
    )
    return response.json()["access_token"]

def test_books_crud():
    token = get_token()

    headers = {"Authorization": f"Bearer {token}"}

    # CREATE
    create = httpx.post(
        f"{BASE_URL}/books/",
        json={
            "title": "Test Book",
            "genre": "Sci-Fi",
            "language": "EN",
            "author_id": 1
        },
        headers=headers
    )
    assert create.status_code == 200
    book = create.json()
    book_id = book["book_id"]

    # READ LIST
    list_resp = httpx.get(f"{BASE_URL}/books/", headers=headers)
    assert list_resp.status_code == 200

    # UPDATE
    upd = httpx.put(
        f"{BASE_URL}/books/{book_id}",
        json={"title": "Updated Test Book"},
        headers=headers
    )
    assert upd.status_code == 200
    assert upd.json()["title"] == "Updated Test Book"

    # DELETE
    delete = httpx.delete(
        f"{BASE_URL}/books/{book_id}",
        headers=headers
    )
    assert delete.status_code == 200
