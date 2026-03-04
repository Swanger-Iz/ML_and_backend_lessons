from database import async_engine, metadata_obj, sync_engine, sync_session_factory
from models import WorkersOrm
from sqlalchemy import insert, text


def create_tables():
    sync_engine.echo = False
    metadata_obj.drop_all(sync_engine)
    metadata_obj.create_all(sync_engine)
    sync_engine.echo = False


def insert_data():
    with sync_session_factory() as session:
        user_steve_rambo = WorkersOrm(username="Steve Rambo")
        user_volk = WorkersOrm(username="Sery Volk")
        session.add_all([user_steve_rambo, user_volk])
        session.commit()


async def async_insert_data():
    with sync_session_factory() as session:
        user_steve_rambo = WorkersOrm(username="Steve Rambo")
        user_volk = WorkersOrm(username="Sery Volk")
        session.add_all([user_steve_rambo, user_volk])
        await session.commit()
