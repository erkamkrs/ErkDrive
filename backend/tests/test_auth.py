import pytest
from httpx import AsyncClient
from backend.app.main import app

@pytest.mark.asyncio
async def test_register_and_login():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Register user
        r = await ac.post("/register", json={"email": "test@example.com", "password": "testpass"})
        assert r.status_code == 200

        # Login user
        r = await ac.post("/login", json={"email": "test@example.com", "password": "testpass"})
        assert r.status_code == 200
        assert "access_token" in r.json()
