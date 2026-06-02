def auth_header(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def test_create_application_strict_status(client):
    # token
    r = client.post("/auth/register", json={"email": "u@example.com", "password": "password123"})
    token = r.json()["access_token"]

    # company
    c = client.post(
        "/companies",
        headers=auth_header(token),
        json={"name": "Google"},
    )
    company_id = c.json()["id"]

    # valid status
    a = client.post(
        "/applications",
        headers=auth_header(token),
        json={"company_id": company_id, "role_title": "SWE Intern", "status": "applied"},
    )
    assert a.status_code == 201
    assert a.json()["status"] == "applied"

    # invalid status should 422 (schema enum validation)
    bad = client.post(
        "/applications",
        headers=auth_header(token),
        json={"company_id": company_id, "role_title": "SWE Intern", "status": "pending"},
    )
    assert bad.status_code == 422