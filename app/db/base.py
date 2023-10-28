from typing import AsyncGenerator

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from app.settings import settings


async_engine = create_async_engine(settings.database_url, echo=settings.echo_sql)
Base = declarative_base()
async_session = async_sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
