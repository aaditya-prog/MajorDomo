from fastapi.testclient import TestClient

<<<<<<< HEAD:APIs/tests/test_user.py
from app.main import app
=======
from main import app
>>>>>>> 94fc5d1aae26a4c0d630759a86ff1e49c20fd853:tests/test_user.py

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
    assert response.json() == {"detail": "Not authenticated"}
