from abc import ABC, abstractmethod
from typing import List

from domain.entities.project import Project, ProjectDashboardSummary


class ProjectRepository(ABC):

    @abstractmethod
    def create(self, project: Project) -> Project:
        pass

    @abstractmethod
    def get_paginated_dashboard_projects(self, user_id: str, page: int, page_size: int) -> tuple[int, List[ProjectDashboardSummary]]:
        pass