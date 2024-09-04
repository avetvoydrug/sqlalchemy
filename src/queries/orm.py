from sqlalchemy import Integer, text, insert, select, func, cast, and_
from database import engine, async_engine, session_factory, Base
from models import WorkersORM, ResumesOrm, Workload
from sqlalchemy.orm import aliased


#expire, refresh, flush
class SyncOrm:
    
    @staticmethod
    def create_tables():
        engine.echo = False
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        engine.echo = True
    
    @staticmethod
    def insert_data():
        worker_bobr = WorkersORM(username='BOBR')
        worker_wolf = WorkersORM(username='Wolf')
        with session_factory() as session:
            session.add_all([worker_bobr, worker_wolf]) # не было запроса в бд
            session.flush() #отправить изменения, но не завершить запрос
            session.commit() # был запрос к бд ||| завершить запрос
    
    @staticmethod
    def insert_resumes():
        with session_factory() as session:
            res_1_wolf = ResumesOrm(
                title='python junior developer', compensation=50000, workload=Workload.fulltime, worker_id=1)
            res_2_wolf = ResumesOrm(
                title='python разработчик', compensation=150000, workload=Workload.fulltime, worker_id=1)
            res_1_gans = ResumesOrm(
                title='python data engineer', compensation=250000, workload=Workload.parttime, worker_id=2)
            res_2_gans = ResumesOrm(
                title='data scientist', compensation=300000, workload=Workload.fulltime, worker_id=2)
            session.add_all([res_1_gans,res_2_gans,
                             res_1_wolf, res_2_wolf])
            session.commit()

    @staticmethod
    def select_resumes_avg_compensation_by_workload(like_language: str):
                        #применяем функцию avg; приводим к int; переназываем, как avg_compensation
        """
        select workload, avg(compensation)::int as avg_compenastion
        from resumes
        where title like '%python%' and compensation > 40000
        group by workload
        """
        with session_factory() as session:
            query = (
                select(
                    ResumesOrm.workload,
                    cast(func.avg(ResumesOrm.compensation), Integer).label("avg_compensation"),
                    # avg: мождно писать, что угодно, если в postgre или другой СУБД нет этой функции, то она вызовется
                )
                .select_from(ResumesOrm) # не обяз//
                # .where/.filter - synonims, /filter_by(что-то=чему-то)
                .filter(and_(
                    ResumesOrm.title.contains(like_language),
                    ResumesOrm.compensation > 40000
                ))
                .group_by(ResumesOrm.workload)
                # .having(cast(func.avg(ResumesOrm.compensation), Integer) > 70000)
            )
            print(query.compile(compile_kwargs={"literal_binds": True}))
            res = session.execute(query)
            result = res.all()
            print(result)

    @staticmethod
    def read_all():
        with session_factory() as session: # конт. менедж. чтобы авто закрывал. сессии и соединения возвращались в БД
            # worker_id = 1
            # worker = session.get(WorkersORM, worker_id) # для работы с одной сущностью
            query = select(WorkersORM)
            result = session.execute(query)
            workers = result.scalars().all()
            print(f"{workers=}")

    @staticmethod
    def update(worker_id: int, new_name: str):
        with session_factory() as ses:
            #1 два запроса, но работаем с объектом питона
            worker = ses.get(WorkersORM, worker_id)
            worker.username = new_name
            #2 один запрос, но в стиле sql

            ses.refresh(worker) # повторный запрос к базе, полезно если какие-то данные были изменены
            # ses.expire(worker) # сбрасывает изменения
            ses.commit()

    @staticmethod
    def join_cte_subquery_window_func(like_language: str = 'python'):
        """
        WITH helper2 AS (
            SELECT *, compensation-avg_worload_compensation AS compensation_diff
            FROM
            (SELECT
                w.id,
                w.username,
                r.compensation,
                r.workload,
                avg(r.compensation) OVER (PARTITION BY worklaod)::int AS avg_workload_compensation
            FROM resuems AS r
            JOIN workers w ON r.workers.id = w.id) helper1
        )
        SELECT * FROM helper2
        ORDER BY compensation_diff DESC;
        """
        with session_factory() as session:
            r = aliased(ResumesOrm)
            w = aliased(WorkersORM)
            subquery = (
                select(
                    r,
                    w,
                    func.avg(r.compensation).over(partition_by=r.workload).cast(Integer).label("avg_workload_compensation")
                )
                # .select_from(r)
                .join(r, r.worker_id == w.id).subquery("helper1")
            )
            cte = (
                select(
                    subquery.c.worker_id,
                    subquery.c.username,
                    subquery.c.compensation,
                    subquery.c.workload,
                    subquery.c.avg_workload_compensation,
                    (subquery.c.compensation - subquery.c.avg_workload_compensation).label("compensation_diff")
                )
                .cte("helper2")
            )
            query = (
                select(cte)
                .order_by(cte.c.compensation_diff.desc())
            )
            res = session.execute(query)
            result = res.all()
            print(f'{result=}')