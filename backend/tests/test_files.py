import pytest
from httpx import AsyncClient
from backend.app.main import app

@pytest.mark.asyncio
async def test_upload_and_list_files(tmp_path):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Register & login
        await ac.post("/register", json={"email": "u1@example.com", "password": "123"})
        token_resp = await ac.post("/login", json={"email": "u1@example.com", "password": "123"})
        token = token_resp.json()["access_token"]

        headers = {"Authorization": f"Bearer {token}"}

        # Upload a file
        file_content = b"Hello World"
        files = {"file": ("test.txt", file_content, "text/plain")}
        r = await ac.post("/upload", headers=headers, files=files)
        assert r.status_code == 200

        # List files
        r = await ac.get("/files", headers=headers)
        assert r.status_code == 200
        assert len(r.json()) > 0
