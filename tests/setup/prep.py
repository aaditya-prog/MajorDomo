from functools import lru_cache

from fastapi.testclient import TestClient

from app.main import app
from app.config.database import Base
from app.dependencies.session import get_db
from .db import create_admin, engine, get_test_session


def overide_db():
    app.dependency_overrides[get_db] = get_test_session


@lru_cache
def get_testing_client() -> TestClient:
    Base.metadata.create_all(engine)
    overide_db()
    create_admin()
    return TestClient(app)
