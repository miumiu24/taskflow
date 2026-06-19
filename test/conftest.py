import pytest_asyncio
from httpx import AsyncClient, ASGITransport

# Импортируем ОРИГИНАЛЬНЫЕ engine, Base и SessionLocal из твоего database.py
from app.database import Base, engine, SessionLocal
from app.main import app

@pytest_asyncio.fixture(autouse=True)
async def prepare_database():
    """Перед каждым тестом сносим базу и создаем заново, используя наш engine"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield

@pytest_asyncio.fixture
async def db_session():
    """Фикстура для тестов. Дает чистую сессию и сохраняет изменения"""
    async with SessionLocal() as session:
        yield session
        await session.commit()

@pytest_asyncio.fixture
async def ac():
    """Создает виртуального клиента для отправки запросов в наше API"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client