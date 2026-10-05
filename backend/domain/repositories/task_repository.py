from abc import ABC, abstractmethod
from typing import List

from domain.entities.task import Task, TaskDashboardSummary


class TaskRepository(ABC):

    @abstractmethod
    def create(self, task: Task)-> Task:
        pass

    @abstractmethod
    def get_by_id(self, task_id: str) -> Task:
        pass

    @abstractmethod
    def change_column(self, task_id: str, column_id: str) -> Task:
        pass

    @abstractmethod
    def get_paginated_dashboard_tasks(self, user_id: str, page: int, page_size: int) -> tuple[int, List[TaskDashboardSummary]]:
        pass