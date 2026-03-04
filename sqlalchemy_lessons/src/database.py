import asyncio

from config import settings
from models import metadata_obj
from sqlalchemy import URL, create_engine, insert, text
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import Session, sessionmaker

# Подключение к БД синхронное
sync_engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=True,  # Логгирование, то есть будет отсылать все запросы в консоль
    pool_size=5,  # кол-во подключений к БД
    max_overflow=10,  # если pool_size исчерпан (запрос висит), то создает еще соединения
)


async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg, echo=True, pool_size=5, max_overflow=10
)

sync_session_factory = sessionmaker(sync_engine)
async_sesion_factory = async_sessionmaker(async_engine)

# with sync_session_factory() as session:
#     ...
