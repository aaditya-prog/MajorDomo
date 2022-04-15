from fastapi.testclient import TestClient

from ..app.routers import user

client = TestClient(user.router)


