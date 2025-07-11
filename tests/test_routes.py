import httpx
import pytest
import asyncio
from typing import AsyncGenerator

from auth.jwt_handler import create_access_token
from models.events import Event


@pytest.fixture(scope="function")
async def access_token() -> str:
    return create_access_token("testuser@packt.com")


@pytest.fixture(scope="function")
async def mock_event() -> AsyncGenerator[Event, None]:
    new_event = Event(
        creator="testuser@packt.com",
        title="FastAPI Book Launch",
        image="https://example.com/image.jpg",
        description="Join us for the launch of the FastAPI book!",
        tags=["FastAPI", "python", "book", "launch"],
        location="Google Meet",
    )
    await new_event.insert()
    yield new_event
    await new_event.delete()


@pytest.mark.asyncio
async def test_get_events(default_client: httpx.AsyncClient, mock_event: Event) -> None:
    response = await default_client.get("/event/")
    assert response.status_code == 200
    assert response.json()[0]["_id"] == str(mock_event.id)


@pytest.mark.asyncio
async def test_get_event(default_client: httpx.AsyncClient, mock_event: Event) -> None:
    url = f"/event/{str(mock_event.id)}"
    response = await default_client.get(url)

    assert response.status_code == 200
    assert response.json()["creator"] == mock_event.creator
    assert response.json()["_id"] == str(mock_event.id)


@pytest.mark.asyncio
async def test_post_event(default_client: httpx.AsyncClient, access_token: str) -> None:
    payload = {
        "title": "Test create FastAPI Book Launch",
        "image": "https://example.com/test-create.jpg",
        "description": "Create document Test",
        "tags": ["FastAPI", "python", "book", "launch"],
        "location": "Google Meet",
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    test_response = {"message": "Event created successfully"}

    response = await default_client.post("/event/new", json=payload, headers=headers)

    assert response.status_code == 200
    assert response.json() == test_response


@pytest.mark.asyncio
async def test_get_events_count(default_client: httpx.AsyncClient) -> None:
    response = await default_client.get("/event/")
    events = response.json()

    assert response.status_code == 200
    assert len(events) == 0


@pytest.mark.asyncio
async def test_update_event(
    default_client: httpx.AsyncClient, mock_event: Event, access_token: str
) -> None:
    test_payload = {
        "title": "Updated FastAPI event",
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    url = f"/event/{str(mock_event.id)}"
    response = await default_client.put(url, json=test_payload, headers=headers)

    assert response.status_code == 200
    assert response.json()["title"] == test_payload["title"]


@pytest.mark.asyncio
async def test_delete_event(
    default_client: httpx.AsyncClient, mock_event: Event, access_token: str
) -> None:
    test_response = {"message": "Event deleted successfully"}

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    url = f"/event/{mock_event.id}"
    response = await default_client.delete(url, headers=headers)

    assert response.status_code == 200
    assert response.json() == test_response


@pytest.mark.asyncio
async def test_delete_event_not_found(
    default_client: httpx.AsyncClient, mock_event: Event
) -> None:
    url = f"/event/{str(mock_event.id)}"
    response = await default_client.get(url)

    assert response.status_code == 200
    assert response.json()["creator"] == mock_event.creator
    assert response.json()["_id"] == str(mock_event.id)
