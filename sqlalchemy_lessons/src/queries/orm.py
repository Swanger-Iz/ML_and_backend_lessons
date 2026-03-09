from database import (
    async_engine,
    async_sesion_factory,
    sync_engine,
    sync_session_factory,
)
from models import Base, ResumeOrm, WorkersOrm, WorkLoad
from sqlalchemy import Integer, and_, cast, func, insert, select, update
from sqlalchemy.orm import aliased, contains_eager, joinedload, selectinload


class SyncOrm:
    def clear_db():
        # ResumeOrm.__table__.drop(sync_engine, checkfirst=True)
        # WorkersOrm.__table__.drop(sync_engine, checkfirst=True)
        Base.metadata.drop_all(sync_engine)

    @staticmethod
    def create_tables():
        Base.metadata.drop_all(sync_engine)
        Base.metadata.create_all(sync_engine)
        sync_engine.echo = True

    @staticmethod
    def insert_data_in_WorkersOrm():
        workers_data = [
            {"username": "Ricardo Milos"},
            {"username": "Dmitry Volkov"},
            {"username": "Alexey Petrov"},
            {"username": "Maria Sokolova"},
            {"username": "Ivan Ivanov"},
            {"username": "Keanu Reeves"},
            {"username": "Ryan Gosling"},
            {"username": "Christian Bale"},
            {"username": "Benedict Cumberbatch"},
            {"username": "Tom Hardy"},
        ]
        with sync_session_factory() as session:
            # user_steve_rambo = WorkersOrm(username="Steve Rambo")
            # user_volk = WorkersOrm(username="Sery Volk")
            # session.add_all([user_steve_rambo, user_volk])
            session.add_all([WorkersOrm(**userdata) for userdata in workers_data])

            session.flush()  # отправляет изнения в БД, не завершая транзакцию
            session.commit()

    @staticmethod
    def select_workers():
        with sync_session_factory() as session:
            # worker_id = 1
            # # Можно передать ключи кортежем
            # # worker_user1 = session.get(WorkersOrm, worker_id)
            q = select(WorkersOrm)
            # result = session.execute(q).all()[0][0]
            result = session.execute(q).scalars().all()
            print(f"SELECT OUT: {result=}")

    @staticmethod
    def update_worker(worker_id: int, new_username: str):
        with sync_session_factory() as session:
            worker_to_change = session.get(WorkersOrm, worker_id)
            worker_to_change.username = new_username

            # session.expire()  # Отменяет все изменения внесенные в БД для одного объекта .expire() или для всех .expire_all()
            session.refresh(worker_to_change)  # .refresh() забирает последние обновления с БД
            session.commit()

    @staticmethod
    def insert_rows_in_ResumeOrm():
        resumes_data = [
            {"title": "DevOps Engineer", "compensation": 280000, "workload": WorkLoad.fulltime, "worker_id": 5},
            {"title": "Backend Developer (Go)", "compensation": 220000, "workload": WorkLoad.fulltime, "worker_id": 6},
            {"title": "Frontend Developer (React)", "compensation": 180000, "workload": WorkLoad.parttime, "worker_id": 7},
            {"title": "QA Automation Engineer", "compensation": 140000, "workload": WorkLoad.fulltime, "worker_id": 8},
            {"title": "ML Engineer", "compensation": 350000, "workload": WorkLoad.fulltime, "worker_id": 9},
            {"title": "Cybersecurity Specialist", "compensation": 260000, "workload": WorkLoad.fulltime, "worker_id": 10},
            {"title": "Product Manager", "compensation": 310000, "workload": WorkLoad.fulltime, "worker_id": 5},
            {"title": "iOS Developer", "compensation": 240000, "workload": WorkLoad.parttime, "worker_id": 10},
            {"title": "Android Developer", "compensation": 230000, "workload": WorkLoad.fulltime, "worker_id": 1},
            {"title": "System Architect", "compensation": 450000, "workload": WorkLoad.fulltime, "worker_id": 2},
            {"title": "Data Engineer", "compensation": 270000, "workload": WorkLoad.fulltime, "worker_id": 3},
            {"title": "UI/UX Designer", "compensation": 160000, "workload": WorkLoad.parttime, "worker_id": 4},
            {"title": "SRE Engineer", "compensation": 290000, "workload": WorkLoad.fulltime, "worker_id": 6},
            {"title": "Fullstack Developer", "compensation": 210000, "workload": WorkLoad.fulltime, "worker_id": 7},
            {"title": "Technical Writer", "compensation": 120000, "workload": WorkLoad.parttime, "worker_id": 9},
        ]
        with sync_session_factory() as session:
            session.add_all([ResumeOrm(**userdata) for userdata in resumes_data])
            session.flush()
            session.commit()

    @staticmethod
    def select_resumes_avg_compensation(like_lang: str):
        """
        select r.workload , AVG(r.compensation )::int as avg_comp
        from resumes r
        where r.title like '%Python%' and r.compensation  > 40000
        group by r.workload;
        """
        with sync_session_factory() as session:
            q = (
                select(
                    ResumeOrm.workload,
                    cast(func.avg(ResumeOrm.compensation), Integer).label("avg_comp"),
                )
                .select_from(ResumeOrm)
                # .where() same .filter(), .filter_by(id=1, workload='fulltime')
                .filter(
                    and_(
                        ResumeOrm.title.contains(like_lang),
                        ResumeOrm.compensation > 40000,
                    )
                )
                .group_by(ResumeOrm.workload)
                .having(cast(func.avg(ResumeOrm.compensation), Integer) > 70000)
            )

            print(q.compile(compile_kwargs={"literal_binds": True}))

            result = session.execute(q).all()
            print(result)

            res_el0 = result[0]
            print(res_el0.avg_comp)

    # При lazy загрузке проблема n + 1 запросов
    @staticmethod
    def select_workers_with_lazy_relashionship():
        with sync_session_factory() as session:
            query = select(WorkersOrm)
            res = session.execute(query).scalars().all()

            worker1 = res[0].resumes
            print(worker1)

            worker2 = res[1].resumes
            print(worker2)

    @staticmethod
    def select_workers_with_joined_relashionship():
        """
        Для случаев, когда у нас отношение one to many | many to one joined не очень подходит, потому что
        мы выгружаем много дубликатов, он подходит когда связь many to one | one to one.
        """
        with sync_session_factory() as session:
            query = select(WorkersOrm).options(joinedload(WorkersOrm.resumes))
            res = session.execute(query).unique().scalars().all()

            worker1 = res[0].resumes
            print(worker1)

            worker2 = res[1].resumes
            print(worker2)

    @staticmethod
    def select_workers_with_selectin_relashionship():
        """
        Для случаев, когда у нас отношение many to many | one to many нужно использовать selectinload, потому что
        мы сначала выгружаем всех уникальные значения, а затем выбираем из всех резюме эти уникальные
        """
        with sync_session_factory() as session:
            query = select(WorkersOrm).options(selectinload(WorkersOrm.resumes))
            res = session.execute(query).scalars().all()

            worker1 = res[0].resumes
            print(worker1)

            worker2 = res[1].resumes
            print(worker2)

    @staticmethod
    def select_workers_with_condition_relationship():
        with sync_session_factory() as session:
            q = select(WorkersOrm).options(selectinload(WorkersOrm.resumes_parttime))
            res = session.execute(q).scalars().all()
            print(res)

    @staticmethod
    def select_workers_with_condition_relationship_contains_eager():
        with sync_session_factory() as session:
            q = select(WorkersOrm).join(WorkersOrm.resumes).options(contains_eager(WorkersOrm.resumes)).filter(ResumeOrm.workload == "parttime")
            res = session.execute(q).unique().scalars().all()
            print(res)


class AsyncOrm:
    @staticmethod
    async def async_insert_data():
        with sync_session_factory() as session:
            user_steve_rambo = WorkersOrm(username="Steve Rambo")
            user_volk = WorkersOrm(username="Sery Volk")
            session.add_all([user_steve_rambo, user_volk])
            await session.commit()

    @staticmethod
    async def insert_data_workers_resumes():
        workers_data = [
            {"username": "Ricardo Milos"},
            {"username": "Dmitry Volkov"},
            {"username": "Alexey Petrov"},
            {"username": "Maria Sokolova"},
            {"username": "Ivan Ivanov"},
            {"username": "Keanu Reeves"},
            {"username": "Ryan Gosling"},
            {"username": "Christian Bale"},
            {"username": "Benedict Cumberbatch"},
            {"username": "Tom Hardy"},
        ]
        resumes_data = [
            {"title": "DevOps Engineer", "compensation": 280000, "workload": WorkLoad.fulltime, "worker_id": 5},
            {"title": "Backend Developer (Go)", "compensation": 220000, "workload": WorkLoad.fulltime, "worker_id": 6},
            {"title": "Frontend Developer (React)", "compensation": 180000, "workload": WorkLoad.parttime, "worker_id": 7},
            {"title": "QA Automation Engineer", "compensation": 140000, "workload": WorkLoad.fulltime, "worker_id": 8},
            {"title": "ML Engineer", "compensation": 350000, "workload": WorkLoad.fulltime, "worker_id": 9},
            {"title": "Cybersecurity Specialist", "compensation": 260000, "workload": WorkLoad.fulltime, "worker_id": 10},
            {"title": "Product Manager", "compensation": 310000, "workload": WorkLoad.fulltime, "worker_id": 5},
            {"title": "iOS Developer", "compensation": 240000, "workload": WorkLoad.parttime, "worker_id": 10},
            {"title": "Android Developer", "compensation": 230000, "workload": WorkLoad.fulltime, "worker_id": 1},
            {"title": "System Architect", "compensation": 450000, "workload": WorkLoad.fulltime, "worker_id": 2},
            {"title": "Data Engineer", "compensation": 270000, "workload": WorkLoad.fulltime, "worker_id": 3},
            {"title": "UI/UX Designer", "compensation": 160000, "workload": WorkLoad.parttime, "worker_id": 4},
            {"title": "SRE Engineer", "compensation": 290000, "workload": WorkLoad.fulltime, "worker_id": 6},
            {"title": "Fullstack Developer", "compensation": 210000, "workload": WorkLoad.fulltime, "worker_id": 7},
            {"title": "Technical Writer", "compensation": 120000, "workload": WorkLoad.parttime, "worker_id": 9},
        ]
        async with async_sesion_factory() as session:
            insert_workers = insert(WorkersOrm).values(workers_data)
            insert_resumes = insert(ResumeOrm).values(resumes_data)

            await session.execute(insert_workers)
            await session.execute(insert_resumes)
            await session.flush()
            await session.commit()

    @staticmethod
    async def join_cte_subquery_window_func(like_lang: str = "Python"):
        """
        with cte as (
        select *, subq.avg_workload_comp - subq.compensation  as compensation_diff
        from
        (select
            w.id ,
            w.username ,
            r.compensation ,
            r.workload,
            AVG(r.compensation) over (partition by r."workload" )::int as avg_workload_comp
        from resumes r
        inner join workers w on r.worker_id = w.id ) as subq
        )
        select * from cte
        order by cte.compensation_diff desc;
        """

        async with async_sesion_factory() as session:
            r = aliased(ResumeOrm)
            w = aliased(WorkersOrm)

            subq = (
                select(r, w, w.id.label("w_id"), func.avg(r.compensation).over(partition_by=r.workload).cast(Integer).label("avg_workload_comp"))
                # .select_from(r, w)
                .join(
                    r, w.id == r.worker_id
                ).subquery(  # parameters. fulljoin: full= | leftjoin: isouter= | rightjoin: его нет | innerjoin: не нужно явно указывать
                    "sbq"
                )
            )
            cte = select(
                subq.c.worker_id,
                subq.c.username,
                subq.c.compensation,
                subq.c.workload,
                subq.c.avg_workload_comp,
                (subq.c.avg_workload_comp - subq.c.compensation).label("compensation_diff"),
            ).cte(
                "cte"
            )  # это все после with as helper2
            query = select(cte).order_by(cte.c.compensation_diff.desc())

            # print(query.compile(compile_kwargs={"literal_binds": True}))

            _ = await session.execute(query)
            result = _.all()
            print(f"{result=}")
