def test_create_client(client):

    login = client.post(
        "/auth/login",
        json={
            "username": "pytest_user",
            "password": "password123"
        }
    )

    token = login.json()["access_token"]

    response = client.post(
        "/clients",
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "client_name": "Pytest Client",
            "time_zone": "Asia/Kolkata",
            "primary_contact": "test@example.com",
            "active_status": True
        }
    )

    assert response.status_code == 200


def test_client_requires_auth(client):

    response = client.post(
        "/clients",
        json={
            "client_name": "Unauthorized Client",
            "time_zone": "Asia/Kolkata",
            "primary_contact": "test@example.com",
            "active_status": True
        }
    )

    assert response.status_code in [401, 403]
