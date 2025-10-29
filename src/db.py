from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

from settings import settings

Base = declarative_base()

engine: AsyncEngine = create_async_engine(settings.database_url)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
    class_=AsyncSession,
)


async def get_async_session() -> AsyncGenerator:
    async with AsyncSessionLocal() as session:
        yield session
