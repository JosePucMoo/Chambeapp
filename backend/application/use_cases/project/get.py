from typing import List

from domain.exceptions.not_found_exception import NotFoundException
from domain.utils.constants import Constants
from domain.entities.project import ProjectBoard, ProjectDashboardSummary, ProjectMember
from domain.repositories.project_repository import ProjectRepository


class GetProjectUseCase:
    def __init__(self, repository: ProjectRepository ):
        self.repository = repository 

    def execute_paginated_summary(self, user_id: str, page: int, page_size: int) -> tuple[int, ProjectDashboardSummary]:
        return self.repository.get_paginated_dashboard_projects(
            user_id=user_id,
            page=page,
            page_size=page_size
        )

    def execute_get_project_members(self, project_id) -> List[ProjectMember]:
        project = self.repository.get_by_id(project_id)

        if not project:
            raise NotFoundException(Constants.PROJECT_NOT_FOUND)

        return self.repository.get_project_members(project_id)

    def execute_get_project_board(self, project_id) -> ProjectBoard:
        project = self.repository.get_by_id(project_id)
        
        if not project:
            raise NotFoundException(Constants.PROJECT_NOT_FOUND)

        return self.repository.get_project_board(project_id)