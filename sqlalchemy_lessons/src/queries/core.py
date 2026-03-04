import asyncio

from database import sync_engine
from models import metadata_obj, workers_table
from sqlalchemy import insert, select, text, update


class SyncCore:

    @staticmethod
    def create_tables():
        sync_engine.echo = False
        metadata_obj.drop_all(sync_engine)
        metadata_obj.create_all(sync_engine)
        sync_engine.echo = True

    @staticmethod
    def insert_workers():
        with sync_engine.connect() as conn:
            stmt = """
                        INSERT INTO workers (username) VALUES
                        ('AO BOBR'),
                        ('OOO Volk');
                """

            stmt = insert(workers_table).values(
                [{"username": name} for name in ["Billy Harringtonov", "Van Darkholmovich"]]
            )
            conn.execute(stmt)
            conn.commit()

    @staticmethod
    def select_workers():
        with sync_engine.connect() as conn:
            q = select(workers_table)  # SELECT * FROM workers
            result = conn.execute(q).all()

            print(f"{result=}")

    @staticmethod
    def update_worker(worker_id: int, new_username: str):
        with sync_engine.connect() as conn:
            # Нельзя писать f строки

            # Метод 1, сырой запрос
            # stmt = text("UPDATE workers SET username=:username WHERE id=:id")
            # stmt = stmt.bindparams(username=new_username, id=worker_id)

            stmt = (
                update(workers_table).values(username=new_username)
                # .where(workers_table.c.id ==worker_id)
                .filter_by(id=worker_id)
            )

            conn.execute(stmt)
            conn.commit()
