from dataclasses import dataclass, field
from datetime import date, datetime
import uuid

from domain.entities.enums import TaskPriorityEnum

@dataclass
class Task:
    title: str
    description: str
    priority: str
    due_date: datetime
    column_id: str
    assignee_id: str

    id: uuid.UUID = field(default_factory=uuid.uuid4)

@dataclass
class TaskBoard:
    id: str
    title: str
    description: str
    priority: TaskPriorityEnum
    due_date: date
    assignee_id: str
    assignee_name: str | None = None