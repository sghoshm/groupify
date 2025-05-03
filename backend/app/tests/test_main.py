# backend/app/tests/test_main.py
import pytest
from httpx import AsyncClient
from backend.app.main import app # Import the main FastAPI app using absolute path

# Use pytest.mark.asyncio to run async tests
@pytest.mark.asyncio
async def test_health_check():
    """Test the basic health check endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

@pytest.mark.asyncio
async def test_read_root():
    """Test the root endpoint."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Groupify Backend"}

# Add more tests for your API endpoints here
# Example:
# @pytest.mark.asyncio
# async def test_signup_user():
#     async with AsyncClient(app=app, base_url="http://test") as ac:
#         signup_data = {"email": "test@example.com", "password": "password123"}
#         response = await ac.post("/api/v1/auth/signup", json=signup_data)
#     assert response.status_code == 200 # Or 201 depending on your implementation
#     assert "user_id" in response.json()
