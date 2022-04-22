from tests.setup.db import user
from tests.setup.prep import get_testing_client

client = get_testing_client()


def test_login():
    breakpoint()
    login = {
        "username": user["username"],
        "password": user["password"]
    }
    breakpoint()
    response = client.post(
        "/user/auth/login",
        data=login
    )
    response_json = response.json()
    breakpoint()
    assert response.status_code == 200
    assert "token" in response_json
    assert response_json["token_type"] == "Bearer"


def test_user_registration_route_is_protected():
    response = client.post(
        "/user/register",
        json={
            "username": "admin",
            "full_name": "John Doe",
            "staff_type": "Inventory Staff",
        },
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "Not authenticated"}
