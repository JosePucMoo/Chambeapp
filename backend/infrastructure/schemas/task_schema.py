
from datetime import datetime

from pydantic import ConfigDict

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

class CreateTaskDTO(BaseTaskDTO):

    model_config= ConfigDict(from_attributes=True)