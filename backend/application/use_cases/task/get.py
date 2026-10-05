from typing import List

from domain.entities.task import TaskDashboardSummary
from domain.repositories.task_repository import TaskRepository


class GetTaskUseCase:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def execute_paginated_summary(self, user_id: str, page: int, page_size: int) -> tuple[int, List[TaskDashboardSummary]]:
        return self.repository.get_paginated_dashboard_tasks(
            user_id=user_id,
            page=page,
            page_size=page_size
        )