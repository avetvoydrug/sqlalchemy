from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

from models import Workload

# class Base_w_repr(BaseModel):
#     def __repr__(self):


class WorkersAddDTO(BaseModel): # data transfer object | Add/POST
    # при разработке API принято сначала делать модель для POST
    # запроса потом наследоваться от неё и делать GET и т.д.
    username: str

class WorkersDTO(WorkersAddDTO):
    # модель для Get запроса
    id: int

class ResumesAddDTO(BaseModel):
    # модель для POST
    title: str
    compensation: Optional[int]
    workload: Workload
    worker_id: int

class ResumesDTO(ResumesAddDTO):
    # Модель для GET
    id: int
    created_at: datetime
    updated_at: datetime


# модели с relationship
class ResumesRelDTO(ResumesDTO):
    worker: "WorkersDTO"

class WorkerRelDTO(WorkersDTO):
    resumes: list["ResumesDTO"]