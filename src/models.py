from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

from enum import Enum
from datetime import datetime
from typing import Annotated

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime, mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.utcnow)]
        #ser_def СУБД устанавливает
        #default - orm отправляет запросы


class WorkersORM(Base):
    __tablename__ = 'workers'

    id: Mapped[intpk]
    username: Mapped[str]

class Workload(Enum):
    fulltime = 'fulltime'
    parttime = 'parttime'

class ResumesOrm(Base):
    __tablename__ = 'resumes'
    # """
    #     id: auotincriment;
    #     title: str
    #     compensation: int
    #     workload: Workload[Enum]
    #     worker_id: foreign_key
    #     created_at: auto
    #     updated_at: auto
    # """
    id: Mapped[intpk] 
    title: Mapped[str]
    compensation: Mapped[int | None]
    workload: Mapped[Workload]
    worker_id: Mapped[int] = mapped_column(ForeignKey("workers.id", ondelete="CASCADE"))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]





metadata = MetaData()

workers = Table(
    'workers',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String)
    )