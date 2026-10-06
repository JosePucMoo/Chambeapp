from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import List

from domain.entities.task import (
    DailyTaskActivity,
    Task,
    TaskDashboardSummary,
    TaskDueSoon,
    TaskMetricsAggregate,
)


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

    @abstractmethod
    def get_metrics(self, user_id: str, due_from: date, due_to: date) -> TaskMetricsAggregate:
        pass

    @abstractmethod
    def get_due_soon_tasks(self, user_id: str, due_from: date, due_to: date) -> List[TaskDueSoon]:
        pass

    @abstractmethod
    def get_weekly_activity(self, user_id: str, start_at: datetime, end_at: datetime) -> List[DailyTaskActivity]:
        pass