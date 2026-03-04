import asyncio

from config import settings
from models import metadata_obj, workers_table
from sqlalchemy import URL, create_engine, insert, text
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import Session, sessionmaker

# Подключение к БД синхронное
engine_sync = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=True,  # Логгирование, то есть будет отсылать все запросы в консоль
    pool_size=5,  # кол-во подключений к БД
    max_overflow=10,  # если pool_size исчерпан (запрос висит), то создает еще соединения
)

# print(settings.DATABASE_URL_psycopg)

# with engine_sync.connect() as conn:
#     res = conn.execute(text("SELECT VERSION()"))
#     print(f"{res.one()=}")
#     conn.commit()

engine_async = create_async_engine(
    url=settings.DATABASE_URL_asyncpg, echo=True, pool_size=5, max_overflow=10
)


async def as_main():
    async with engine_async.connect() as conn:
        res = await conn.execute(text("SELECT VERSION()"))
        print(f"{res.one()=}")
        # conn.commit()


# asyncio.run(as_main())


def insert_data():
    with engine_sync.connect() as conn:
        # stmt = """
        #         INSERT INTO workers (username) VALUES
        #         ('AO BOBR'),
        #         ('OOO Volk');
        # """

        stmt = insert(workers_table).values(
            [{"username": name} for name in ["Billy Harringtonov", "Van Darkholmovich"]]
        )
        conn.execute(stmt)
        conn.commit()
