import pytest
from fastapi.testclient import TestClient
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models.database import Base
from app.models.entities import Order, OrderItem, User
from app.controllers.dependencies import get_db
from app.main import app
import asyncio

DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Cria o engine assíncrono para testes
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture(scope="session")
def engine():
    return create_async_engine(DATABASE_URL, future=True)

@pytest_asyncio.fixture(scope="session")
async def tables(engine):
    async with engine.begin() as conn:
        await conn.run_sync(
            lambda sync_conn: Base.metadata.create_all(
                sync_conn,
                tables=[User.__table__, Order.__table__, OrderItem.__table__]
            )
        )
    yield
    async with engine.begin() as conn:
        await conn.run_sync(
            lambda sync_conn: Base.metadata.drop_all(
                sync_conn,
                tables=[User.__table__, Order.__table__, OrderItem.__table__]
            )
        )

@pytest_asyncio.fixture(scope="function")
async def db_session(engine, tables):
    async_session = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    async with async_session() as session:
        yield session

@pytest.fixture(scope="function")
def client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
