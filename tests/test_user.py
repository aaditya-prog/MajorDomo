from app.schemas.user import Staff
from tests.setup.db import generate_dummy_user
from tests.setup.prep import get_testing_client

client = get_testing_client()


# Try to log in with user that is not present in database
def test_login_invalid_user():
    login = {
        "username": "random",
        "password": "random"
    }
    response = client.post(
        "/user/auth/login",
        data=login
    )
    response_json = response.json()
    assert response.status_code == 404
    assert response_json["detail"] == "User does not exists"


# Try to log in with wrong password
def test_login_invalid_password():
    login = {
        "username": "Admin",
        "password": "random_password"
    }
    response = client.post(
        "/user/auth/login",
        data=login
    )
    response_json = response.json()
    assert response.status_code == 401
    assert response_json["detail"] == "Incorrect Password, try again."


# Accessing "Register" Endpoint without token.
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


# Log in with valid user
def test_login():
    user = generate_dummy_user(Staff.ADMIN)
    login = {
        "username": user["username"],
        "password": user["password"]
    }
    response = client.post(
        "/user/auth/login",
        data=login
    )
    response_json = response.json()
    assert response.status_code == 200
    assert "token" in response_json
    assert response_json["token_type"] == "Bearer"
