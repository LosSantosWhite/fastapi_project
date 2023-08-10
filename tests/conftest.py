import asyncio
from io import BufferedReader
import json
import os
from typing import Generator

from fastapi import UploadFile
import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import sessionmaker

from app.config import config
from app.db.postgresql.base import Base
from app.db.postgresql.dependencies import get_async_session
from app.entrypoints.main import create_app

fixtures_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fixtures")

pytest_plugins = [
    f"tests.fixtures.{filename.split('.')[0]}"
    for filename in os.listdir(fixtures_folder)
    if not filename.startswith("_")
]


@pytest.fixture(scope="session")
def event_loop(request) -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close


@pytest_asyncio.fixture(scope="session")
async def _db_connection() -> Generator:
    async_engine = create_async_engine(
        config.postgresql.using_async_driver_for_test, echo=False, future=True
    )
    async with async_engine.connect() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()
        yield conn
        await conn.run_sync(Base.metadata.drop_all)
        await conn.commit()

    await async_engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def _async_session(_db_connection: AsyncConnection) -> AsyncSession:
    session = sessionmaker(
        bind=_db_connection,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with session() as s:
        s.commit = s.flush
        yield s
        await s.rollback()


@pytest_asyncio.fixture(scope="function")
async def _async_client_as_staff(_async_session: AsyncSession) -> AsyncClient:
    app = create_app()
    app.dependency_overrides[get_async_session] = lambda: _async_session

    async with AsyncClient(
        app=app,
        base_url=f"http://{config.prefixes.admin}",
        headers={"access_token": config.security.key},
    ) as client:
        yield client


@pytest.fixture(scope="function")
def _test_data() -> dict:
    path = os.getenv("PYTEST_CURRENT_TEST")
    path = os.path.join(*os.path.split(path)[:-1], "data", "data.json")

    if not os.path.exists(path):
        path = os.path.join("data", "data.json")

    with open(path, "r") as file:
        data = json.loads(file.read())

    return data


@pytest.fixture(scope="function")
def _test_image_entity() -> BufferedReader:
    path = os.getenv("PYTEST_CURRENT_TEST")
    path = os.path.join(*os.path.split(path)[:-1], "data", "test_image.png")

    if not os.path.exists(path):
        path = os.path.join("data", "test_image.png")

    with open(path, "rb") as file_obj:
        yield file_obj
