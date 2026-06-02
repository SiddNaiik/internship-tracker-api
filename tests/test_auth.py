def test_register_and_login(client):
    # register
    r = client.post("/auth/register", json={"email": "a@example.com", "password": "password123"})
    assert r.status_code == 201
    token = r.json()["access_token"]
    assert token

    # login
    r2 = client.post("/auth/login", json={"email": "a@example.com", "password": "password123"})
    assert r2.status_code == 200
    token2 = r2.json()["access_token"]
    assert token2