from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool

# 1. Меняем протокол на +asyncpg
SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:1@db:5432/taskflow_db"

# 2. Создаем асинхронный движок (create_async_engine)
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,
    poolclass=NullPool
)
# 3. Создаем фабрику асинхронных сессий (AsyncSession)
SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False  # Чтобы объекты не "протухали" после сохранения
)

# Наш базовый класс для моделей остается прежним
class Base(DeclarativeBase):
    pass