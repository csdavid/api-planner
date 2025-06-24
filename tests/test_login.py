import httpx
import pytest
from typing import AsyncGenerator
from models.users import User
from auth.hash_password import HashPassword


@pytest.fixture(scope="function")
async def mock_user() -> AsyncGenerator[User, None]:
    new_user = User(
        email="testuser@packt.com",
        password=HashPassword().create_hash("testpassword"),
        events=[],
    )
    await new_user.insert()
    yield new_user
    await new_user.delete()


@pytest.mark.asyncio
async def test_sign_new_user(default_client: httpx.AsyncClient) -> None:
    payload = {
        "email": "testuser@packt.com",
        "password": "testpassword",
        "events": [],
    }

    headers = {"accept": "application/json", "Content-Type": "application/json"}

    test_response = {"message": "User created successfully"}

    response = await default_client.post("/user/signup", json=payload, headers=headers)

    assert response.status_code == 200
    assert response.json() == test_response


@pytest.mark.asyncio
async def test_signin_user_in(
    default_client: httpx.AsyncClient, mock_user: User
) -> None:
    payload = {
        "username": "testuser@packt.com",
        "password": "testpassword",
    }

    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = await default_client.post("/user/signin", data=payload, headers=headers)
    assert response.status_code == 200
    assert response.json()["token_type"] == "Bearer"
    assert "access_token" in response.json()
