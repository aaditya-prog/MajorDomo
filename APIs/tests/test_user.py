from fastapi.testclient import TestClient

from ..app.main import app

client = TestClient(app)


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
    assert response.json() == {
        "detail": "Not authenticated"
    }
