
from datetime import date, datetime

from pydantic import ConfigDict, Field

from domain.entities.enums import TaskPriorityEnum
from infrastructure.schemas.base_schema import BaseSchema

class BaseTaskDTO(BaseSchema):
    title: str
    description: str
    priority: TaskPriorityEnum
    due_date: datetime
    column_id: str
    assignee_id: str

class TaskResponseDTO(BaseTaskDTO):
    id: str
    
    model_config= ConfigDict(from_attributes=True)

class CreateTaskDTO(BaseSchema):
    title: str = Field(min_length=3, max_length=50)
    description: str
    priority: TaskPriorityEnum
    due_date: datetime
    assignee_id: str

    model_config= ConfigDict(from_attributes=True)

class TaskBoardDTO(BaseSchema):
    id: str
    title: str
    description: str
    priority: TaskPriorityEnum
    due_date: date
    assignee_id: str
    assignee_name: str

class TaskMoveDTO(BaseSchema):
    column_id: str

class TaskDashboardSummaryDTO(BaseSchema):
    id: str
    title: str
    project_title: str
    due_date: datetime
    priority: TaskPriorityEnum
    column_title: str