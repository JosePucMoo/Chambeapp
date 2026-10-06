from dataclasses import dataclass, field
from typing import List

from domain.entities.enums import ProjectStatusEnum


@dataclass
class ProjectStatusCount:
    status: ProjectStatusEnum
    total: int


@dataclass
class WeeklyPerformance:
    name: str
    completed: int
    created: int


@dataclass
class DashboardMetrics:
    total_projects: int
    projects_by_status: List[ProjectStatusCount]
    total_tasks: int
    completed_tasks: int
    tasks_due_soon: int
    weekly_performance: List[WeeklyPerformance] = field(default_factory=list)
