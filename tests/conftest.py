import pytest
from fastapi.testclient import TestClient


# Use autouse=True here to force read and apply app.settings
@pytest.fixture(autouse=True)
def app():
    from app.main import app

    return app


@pytest.fixture
def client(app):
    client = TestClient(app)
    return client
