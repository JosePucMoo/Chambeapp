from typing import List, Optional

from domain.exceptions.not_found_exception import NotFoundException
from domain.utils.constants import Constants
from domain.entities.project import (
    Project,
    ProjectBoard,
    ProjectDashboardSummary,
    ProjectFilters,
    ProjectMember,
)
from domain.entities.task import TaskFilters
from domain.repositories.project_repository import ProjectRepository


class GetProjectUseCase:
    def __init__(self, repository: ProjectRepository):
        self.repository = repository

    def execute_paginated_summary(
        self, user_id: str, page: int, page_size: int, filters: Optional[ProjectFilters] = None
    ) -> tuple[int, List[ProjectDashboardSummary]]:
        return self.repository.get_paginated_dashboard_projects(
            user_id=user_id, page=page, page_size=page_size, filters=filters
        )

    def execute_get_project_members(self, project_id) -> List[ProjectMember]:
        project = self.repository.get_by_id(project_id)

        if not project:
            raise NotFoundException(Constants.PROJECT_NOT_FOUND)

        return self.repository.get_project_members(project_id)

    def execute_get_project_board(
        self, project_id, filters: Optional[TaskFilters] = None
    ) -> Optional[ProjectBoard]:
        project = self.repository.get_by_id(project_id)

        if not project:
            raise NotFoundException(Constants.PROJECT_NOT_FOUND)

        return self.repository.get_project_board(project_id, filters=filters)

    def execute(self, project_id: str) -> Project:
        project = self.repository.get_by_id(project_id)

        if not project:
            raise NotFoundException(Constants.PROJECT_NOT_FOUND)

        return project
