from typing import List

from domain.entities.dashboard import DashboardMetrics, ProjectStatusCount
from domain.entities.enums import ProjectStatusEnum
from domain.entities.task import TaskDueSoon
from infrastructure.schemas.base_schema import BaseSchema
from infrastructure.schemas.task_schema import TaskDashboardSummaryDTO


class ProjectStatusCountDTO(BaseSchema):
    status: ProjectStatusEnum
    total: int

    @classmethod
    def from_entity(cls, entity: ProjectStatusCount) -> "ProjectStatusCountDTO":
        return cls(
            status=entity.status,
            total=entity.total
        )


class DueSoonTaskDTO(TaskDashboardSummaryDTO):

    @classmethod
    def from_entity(cls, task: TaskDueSoon) -> "DueSoonTaskDTO":
        return cls(
            id=task.id,
            title=task.title,
            project_title=task.project_title,
            due_date=task.due_date,
            priority=task.priority,
            column_title=task.column_title
        )


class WeeklyPerformanceDTO(BaseSchema):
    name: str
    completed: int
    created: int

    @classmethod
    def from_entity(cls, name: str, completed: int, created: int) -> "WeeklyPerformanceDTO":
        return cls(
            name=name,
            completed=completed,
            created=created
        )


class DashboardResponseDTO(BaseSchema):

    @classmethod
    def from_entity(cls, metrics: DashboardMetrics) -> "DashboardResponseDTO":
        return cls(
            total_projects=metrics.total_projects,
            projects_by_status=[
                ProjectStatusCountDTO.from_entity(item)
                for item in metrics.projects_by_status
            ],
            total_tasks=metrics.total_tasks,
            completed_tasks=metrics.completed_tasks,
            tasks_due_soon=metrics.tasks_due_soon,
            weekly_performance=[
                WeeklyPerformanceDTO.from_entity(
                    name=item.name,
                    completed=item.completed,
                    created=item.created
                )
                for item in metrics.weekly_performance
            ]
        )

    total_projects: int
    projects_by_status: List[ProjectStatusCountDTO]
    total_tasks: int
    completed_tasks: int
    tasks_due_soon: int
    weekly_performance: List[WeeklyPerformanceDTO]
