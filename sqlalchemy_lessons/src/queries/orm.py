from database import async_engine, sync_engine, sync_session_factory
from models import Base, WorkersOrm
from sqlalchemy import select, update


class SyncOrm:
    def clear_db():
        Base.metadata.drop_all(sync_engine)

    def create_tables():
        Base.metadata.drop_all(sync_engine)
        Base.metadata.create_all(sync_engine)
        sync_engine.echo = True

    def insert_data():
        with sync_session_factory() as session:
            user_steve_rambo = WorkersOrm(username="Steve Rambo")
            user_volk = WorkersOrm(username="Sery Volk")
            session.add_all([user_steve_rambo, user_volk])
            session.commit()

    @staticmethod
    def select_workers():
        with sync_session_factory() as session:
            # worker_id = 1
            # # Можно передать ключи кортежем
            # # worker_user1 = session.get(WorkersOrm, worker_id)
            q = select(WorkersOrm)
            result = session.execute(q).all()
            print(f"{result=}")

    @staticmethod
    def update_worker(worker_id: int, new_username: str):
        with sync_engine.connect() as conn:
            ...

    async def async_insert_data():
        with sync_session_factory() as session:
            user_steve_rambo = WorkersOrm(username="Steve Rambo")
            user_volk = WorkersOrm(username="Sery Volk")
            session.add_all([user_steve_rambo, user_volk])
            await session.commit()
