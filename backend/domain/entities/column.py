from dataclasses import dataclass, field
from typing import List
import uuid

from domain.entities.task import TaskBoard

@dataclass
class Column:
    title: str
    position: int
    project_id: str

    id: uuid.UUID = field(default_factory=uuid.uuid4)

@dataclass
class ColumnBoard:
    id: str
    title: str
    position: int
    tasks: List[TaskBoard]