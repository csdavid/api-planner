import asyncio
import httpx
import pytest

from main import app
from database.connection import Settings
from models.events import Event
from models.users import User


@pytest.fixture(scope="function")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


async def init_db():
    test_settings = Settings()
    test_settings.DATABASE_URL = "mongodb://localhost:27017/planner"

    await test_settings.initialize_database()


@pytest.fixture(scope="function")
async def default_client():
    await init_db()
    async with httpx.AsyncClient(base_url="http://localhost:8080") as client:
        yield client
        # Clean up resources
        await Event.find_all().delete()
        await User.find_all().delete()
