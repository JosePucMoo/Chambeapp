from abc import ABC, abstractmethod
from datetime import date, datetime
from typing import List

from domain.entities.task import (
    DailyTaskActivity,
    Task,
    TaskDashboardSummary,
    TaskDetail,
    TaskDueSoon,
    TaskFilters,
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
    def get_detail_by_id(self, user_id: str, task_id: str) -> TaskDetail:
        pass

    @abstractmethod
    def change_column(self, task_id: str, column_id: str) -> Task:
        pass

    @abstractmethod
    def update(self, user_id: str, task: Task) -> Task:
        pass

    @abstractmethod
    def delete(self, user_id: str, task_id: str) -> bool:
        pass

    @abstractmethod
    def delete_many(self, user_id: str, task_ids: List[str]) -> List[str]:
        pass

    @abstractmethod
    def get_paginated_dashboard_tasks(self, user_id: str, page: int, page_size: int, filters: TaskFilters = None) -> tuple[int, List[TaskDashboardSummary]]:
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