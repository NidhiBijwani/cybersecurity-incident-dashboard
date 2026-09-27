def get_token(client):

    # Create a test user
    client.post(
        "/register",
        json={
            "username": "incident_test_user",
            "email": "incident_test@example.com",
            "password": "testpassword123"
        }
    )

    response = client.post(
        "/login",
        data={
            "username": "incident_test_user",
            "password": "testpassword123"
        }
    )

    assert response.status_code == 200

    return response.json()["access_token"]


def test_get_incidents(client):

    token = get_token(client)

    response = client.get(
        "/incidents",
        headers={
            "Authorization":
                f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list
    )


def test_create_incident(client):

    token = get_token(client)

    response = client.post(
        "/incidents",
        headers={
            "Authorization":
                f"Bearer {token}"
        },
        json={
            "incident_type":
                "Test Security Incident",

            "source":
                "127.0.0.1",

            "severity":
                "High",

            "description":
                "Automated test incident",

            "failed_logins":
                10,

            "request_count":
                200,

            "connection_count":
                50,

            "bytes_transferred":
                10000
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["incident_type"] == \
        "Test Security Incident"

    assert data["severity"] == "High"

    assert "risk_score" in data

    assert data["status"] == "Open"


def test_update_incident_status(client):

    token = get_token(client)

    create_response = client.post(
        "/incidents",
        headers={
            "Authorization":
                f"Bearer {token}"
        },
        json={
            "incident_type":
                "Status Test",

            "source":
                "127.0.0.2",

            "severity":
                "Medium",

            "description":
                "Testing status update",

            "failed_logins":
                1,

            "request_count":
                20,

            "connection_count":
                5,

            "bytes_transferred":
                1000
        }
    )

    assert create_response.status_code == 200

    incident_id = (
        create_response.json()["id"]
    )

    response = client.patch(
        f"/incidents/{incident_id}/status",
        headers={
            "Authorization":
                f"Bearer {token}"
        },
        json={
            "status": "Closed"
        }
    )

    assert response.status_code == 200

    assert response.json()["status"] == \
        "Closed"


def test_delete_incident(client):

    token = get_token(client)

    create_response = client.post(
        "/incidents",
        headers={
            "Authorization":
                f"Bearer {token}"
        },
        json={
            "incident_type":
                "Delete Test",

            "source":
                "127.0.0.3",

            "severity":
                "Low",

            "description":
                "Testing deletion",

            "failed_logins":
                0,

            "request_count":
                10,

            "connection_count":
                2,

            "bytes_transferred":
                500
        }
    )

    assert create_response.status_code == 200

    incident_id = (
        create_response.json()["id"]
    )

    response = client.delete(
        f"/incidents/{incident_id}",
        headers={
            "Authorization":
                f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    assert response.json()["message"] == \
        "Incident deleted successfully"


def test_unauthorized_access(client):

    response = client.get(
        "/incidents"
    )

    assert response.status_code == 401