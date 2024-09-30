from typing import Annotated
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase
from sqlalchemy import URL, String, create_engine, text

from config import settings

engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=True,
    # pool_size=5,
    # max_overflow=10
)

async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=False,
    # pool_size=5,
    # max_overflow=10
)

session_factory = sessionmaker(engine)
async_session_factory = async_sessionmaker(async_engine)

str_256 = Annotated[str, 256]

class Base(DeclarativeBase):
    type_annotation_map = {
        str_256: String(256)
    }

    repr_cols_num = 3 # дэфолтное кол-во столбцов на вывод в репр
    repr_cols = tuple() # переопределить в модели => можно добавить доп столбцы на вывод

    def __repr__(self):
        """
            Relationships не используется в repr(), могут вести к неожиданным подгрузкам
            в async версии мы не можем использовать lazy load (всегда писать joined/selectinload)
        """
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            # если доп столбец добавлен или кол-во столбцов не вышло за грань дэфолта
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")
        return f"\n<{self.__class__.__name__} {','.join(cols)}>\n"