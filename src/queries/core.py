import asyncio
from sqlalchemy import text, insert, update
from database import async_engine, engine

from models import metadata, workers

# Core/ORM разница в том, что используем не модель, а таблицу
# и формат возвращаемых данных модели либо стобцы соответственно

# async def get_123():
#     async with async_engine.connect() as conn: # begin/connect b-делает коммит
#         res = await conn.execute(text("SELECT 123 union select 456")) 
#         # сырые запросы ускоряют работу алхимии
#         # но это редко требуется
#         print(f"{res.all()} ")

class SyncCore():
    @staticmethod
    def create_tables():
        engine.echo = False
        metadata.drop_all(engine)
        metadata.create_all(engine)
        engine.echo = True

    @staticmethod
    def insert_data():
        with engine.connect() as conn:
            # stmt = """INSERT INTO workers (username) VALUES
            #         ('Bobr'),
            #         ('Volk');"""
            stmt = insert(workers).values([
                    {"username": "Bobr pidor"},
                    {"username": "Volk petuh"},])
            conn.execute(stmt)
            conn.commit()
    
    @staticmethod
    def read_all():
        with engine.connect() as conn: # begin/connect b-делает коммит
            res = conn.execute(text("SELECT * from workers")) 
            # сырые запросы ускоряют работу алхимии
            # но это редко требуется
            print(f"{res.all()} ") 

    @staticmethod
    def update_name(workers_id: int=1, name: str = 'Mikhel'):
        with engine.connect() as conn:
            #нельзя писать f строки, нужно использовать bindparams от sql-инъекции
            # stmt = text("UPDATE workers SET username=:username WHERE id=:id")
            # stmt = stmt.bindparams(username=name, id=workers_id)
            stmt = (
                update(workers)
                .values(username=name)
                # .where(workers.c.id==workers_id)
                .filter_by(id=workers_id)
            )   
            conn.execute(stmt)
            conn.commit()
