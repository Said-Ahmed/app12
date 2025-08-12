import asyncio
import json

import pytest
from sqlalchemy import insert
from fastapi.testclient import TestClient

from src.auth.models import Users
from src.config import settings
from src.database import engine, Base, async_session_maker
from src.posts.models import Posts
from src.main import app as fastapi_app


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def client():
    yield TestClient(fastapi_app, base_url="http://test")


@pytest.fixture(scope="session")
def authenticated_admin():
    client = TestClient(fastapi_app, base_url="http://test")
    assert client.post("auth/register/", json={
        "first_name": "Администратор",
        "last_name": "Админ",
        "email": "admin@gmail.com",
        "password": "admin123",
        "password_repeat": "admin123",
        "is_admin": True
    })
    client.post("/auth/login", json={
        "email": "admin@gmail.com",
        "password": "admin123"
    })
    assert client.cookies["access_token"]
    yield client


@pytest.fixture(scope="session")
def authenticated_client():
    client = TestClient(fastapi_app, base_url="http://test")
    assert client.post("auth/register/", json={
        "first_name": "Иван",
        "last_name": "Иванов",
        "email": "user@gmail.com",
        "password": "123",
        "password_repeat": "123",
        "is_admin": False
    })
    client.post("/auth/login", json={
        "email": "user@gmail.com",
        "password": "123"
    })
    assert client.cookies["access_token"]
    yield client


@pytest.fixture(scope="function")
async def session():
    async with async_session_maker() as session:
        yield session
