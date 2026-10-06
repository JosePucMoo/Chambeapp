from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional
import uuid

from domain.entities.enums import TaskPriorityEnum

@dataclass
class Task:
    title: str
    description: str
    priority: str
    due_date: datetime
    assignee_id: str
    column_id: Optional[str] = None

    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None

@dataclass
class TaskBoard:
    id: str
    title: str
    description: str
    priority: TaskPriorityEnum
    due_date: date
    assignee_id: str
    assignee_name: str | None = None

@dataclass
class TaskDashboardSummary:
    id: str
    title: str
    project_title: str
    priority: TaskPriorityEnum
    due_date: date
    column_title: str

@dataclass
class TaskDetail:
    id: str
    title: str
    description: str
    priority: TaskPriorityEnum
    due_date: date
    column_id: str
    column_title: str
    project_id: str
    project_title: str
    assignee_id: str
    assignee_name: str | None = None

@dataclass
class TaskFilters:
    priority: Optional[TaskPriorityEnum] = None
    column_title: Optional[str] = None
    project_id: Optional[str] = None
    search: Optional[str] = None

@dataclass
class TaskMetricsAggregate:
    total_tasks: int = 0
    completed_tasks: int = 0
    tasks_due_soon: int = 0

@dataclass
class DailyTaskActivity:
    day: date
    completed: int = 0
    created: int = 0

@dataclass
class TaskDueSoon:
    id: str
    title: str
    project_title: str
    priority: TaskPriorityEnum
    due_date: date
    column_title: str

