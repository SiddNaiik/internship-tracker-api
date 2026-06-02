def auth_header(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def test_create_and_list_companies(client):
    # get token
    r = client.post("/auth/register", json={"email": "c@example.com", "password": "password123"})
    token = r.json()["access_token"]

    # create company
    r2 = client.post(
        "/companies",
        headers=auth_header(token),
        json={"name": "OpenAI", "website": "https://openai.com", "notes": "Dream company"},
    )
    assert r2.status_code == 201
    company_id = r2.json()["id"]

    # list
    r3 = client.get("/companies", headers=auth_header(token))
    assert r3.status_code == 200
    items = r3.json()
    assert len(items) == 1
    assert items[0]["id"] == company_id
    assert items[0]["name"] == "OpenAI"