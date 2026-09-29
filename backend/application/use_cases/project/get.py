from domain.entities.project import ProjectDashboardSummary
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