from datetime import date
from typing import List

from domain.entities.task import CalendarTask, TaskDashboardSummary, TaskDetail, TaskFilters
from domain.exceptions.not_found_exception import NotFoundException
from domain.repositories.task_repository import TaskRepository
from domain.utils.constants import Constants


class GetTaskUseCase:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def execute_paginated_summary(
        self, user_id: str, page: int, page_size: int, filters: TaskFilters = None
    ) -> tuple[int, List[TaskDashboardSummary]]:
        return self.repository.get_paginated_dashboard_tasks(
            user_id=user_id, page=page, page_size=page_size, filters=filters
        )

    def execute_calendar(
        self, user_id: str, start_date: date, end_date: date, filters: TaskFilters = None
    ) -> List[CalendarTask]:
        return self.repository.get_calendar_tasks(
            user_id=user_id, start_date=start_date, end_date=end_date, filters=filters
        )

    def execute_detail(self, user_id: str, task_id: str) -> TaskDetail:
        task = self.repository.get_detail_by_id(user_id=user_id, task_id=task_id)

        if not task:
            raise NotFoundException(Constants.TASK_NOT_FOUND)

        return task
