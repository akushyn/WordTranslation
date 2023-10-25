import logging
from typing import Annotated, AsyncIterator
from sqlalchemy.orm import DeclarativeBase
from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.settings import settings

logger = logging.getLogger(__name__)

async_engine = create_async_engine(
    settings.database_url,
    pool_pre_ping=True,
    echo=settings.echo_sql,
)
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
    future=True,
)


async def get_session() -> AsyncIterator[async_sessionmaker]:
    try:
        yield AsyncSessionLocal
    except SQLAlchemyError as e:
        logger.exception(e)


AsyncSession = Annotated[async_sessionmaker, Depends(get_session)]


class Base(DeclarativeBase):
    __abstract__ = True
