from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.project import (
    Project,
    ProjectBoard,
    ProjectDashboardSummary,
    ProjectFilters,
    ProjectMember,
)
from domain.entities.task import TaskFilters


class ProjectRepository(ABC):
    @abstractmethod
    def create(self, project: Project) -> Project:
        pass

    @abstractmethod
    def get_paginated_dashboard_projects(
        self,
        user_id: str,
        page: int,
        page_size: int,
        filters: Optional[ProjectFilters] = None,
    ) -> tuple[int, List[ProjectDashboardSummary]]:
        pass

    @abstractmethod
    def get_user_project_summaries(self, user_id: str) -> List[ProjectDashboardSummary]:
        pass

    @abstractmethod
    def get_project_members(self, project_id: str) -> List[ProjectMember]:
        pass

    @abstractmethod
    def get_by_id(self, project_id: str) -> Project:
        pass

    @abstractmethod
    def get_project_board(
        self, project_id: str, filters: Optional[TaskFilters] = None
    ) -> Optional[ProjectBoard]:
        pass
