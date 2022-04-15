from fastapi.testclient import TestClient

from ..app.routers import user

client = TestClient(user.router)


def test_register():
    response = client.post(
        "/register",
        json={
            "username": "admin",
            "full_name": "John Doe",
            "staff_type": "Inventory Staff",
        },
    )
    assert response.status_code == 200
    assert response.json() == {"detail": "User account created."}
