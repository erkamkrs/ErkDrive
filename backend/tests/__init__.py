import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.auth import create_access_token

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def test_user():
    return {
        "email": "test@example.com",
        "password": "testpassword"
    }

@pytest.fixture
def auth_token(test_user):
    return create_access_token({"sub": test_user["email"]})