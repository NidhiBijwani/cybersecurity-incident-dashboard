def test_register_user(client):

    username = "testuser_auth"
    email = "testuser_auth@example.com"

    response = client.post(
        "/register",
        json={
            "username": username,
            "email": email,
            "password": "testpassword123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == username
    assert data["email"] == email


def test_login(client):

    # Create a user first
    client.post(
        "/register",
        json={
            "username": "login_test_user",
            "email": "login_test@example.com",
            "password": "testpassword123"
        }
    )

    response = client.post(
        "/login",
        data={
            "username": "login_test_user",
            "password": "testpassword123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_invalid_login(client):

    # Create a user first
    client.post(
        "/register",
        json={
            "username": "invalid_login_user",
            "email": "invalid_login@example.com",
            "password": "testpassword123"
        }
    )

    response = client.post(
        "/login",
        data={
            "username": "invalid_login_user",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401