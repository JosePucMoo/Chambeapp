from datetime import datetime
from typing import List

from pydantic import ConfigDict, Field

from infrastructure.schemas.column_schema import ColumnBoardDTO
from infrastructure.schemas.task_schema import TaskBoardDTO
from domain.entities.project import ProjectBoard
from infrastructure.schemas.base_schema import BaseSchema


class BaseProjectDTO(BaseSchema):
    title: str = Field(min_length=3, max_length=50)
    description: str
    client: str
    delivery_date: datetime


class CreateProjectDTO(BaseProjectDTO):
    model_config = ConfigDict(from_attributes=True)


class ProjectResponseDTO(BaseProjectDTO):
    id: str

    model_config = ConfigDict(from_attributes=True)


class ProjectDashboardSummaryDTO(BaseSchema):
    id: str
    title: str
    client: str
    role: str
    delivery_date: datetime
    status: str
    progress_percentage: float


class ProjectMemberResponseDTO(BaseSchema):
    id: str
    name: str
    email: str


class ProjectBoardDTO(BaseSchema):
    project_id: str
    project_title: str
    columns: List[ColumnBoardDTO]

    @classmethod
    def from_entity(cls, entity: ProjectBoard) -> "ProjectBoardDTO":
        return cls(
            project_id=entity.project_id,
            project_title=entity.project_title,
            columns=[
                ColumnBoardDTO(
                    id=col.id,
                    title=col.title,
                    position=col.position,
                    tasks=[
                        TaskBoardDTO(
                            id=task.id,
                            title=task.title,
                            description=task.description,
                            priority=task.priority,
                            due_date=task.due_date,
                            assignee_id=task.assignee_id,
                            assignee_name=task.assignee_name,
                        )
                        for task in col.tasks
                    ],
                )
                for col in entity.columns
            ],
        )
