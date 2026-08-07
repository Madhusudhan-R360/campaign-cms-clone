import uuid


def test_register_user(client):

    username = f"pytest_{uuid.uuid4().hex}"

    response = client.post(
        "/auth/register",
        json={
            "username": username,
            "password": "password123"
        }
    )

    assert response.status_code == 200


def test_login_user(client):

    username = f"pytest_{uuid.uuid4().hex}"

    client.post(
        "/auth/register",
        json={
            "username": username,
            "password": "password123"
        }
    )

    response = client.post(
        "/auth/login",
        json={
            "username": username,
            "password": "password123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data