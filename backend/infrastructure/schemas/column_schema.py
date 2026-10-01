
from typing import List

from infrastructure.schemas.task_schema import TaskBoardDTO
from infrastructure.schemas.base_schema import BaseSchema


class CreateColumnDTO(BaseSchema):
    title: str
    position: int

class ColumnResponseDTO(BaseSchema):
    id: str
    title: str
    position: int
    project_id: str

class ColumnBoardDTO(BaseSchema):
    id: str
    title: str
    position: int
    tasks: List[TaskBoardDTO] = [] 