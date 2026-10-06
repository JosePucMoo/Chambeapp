from datetime import date, datetime, time, timedelta
from typing import List

from domain.entities.dashboard import (
    DashboardMetrics,
    ProjectStatusCount,
    WeeklyPerformance,
)
from domain.entities.enums import ProjectStatusEnum
from domain.entities.task import TaskDueSoon
from domain.repositories.project_repository import ProjectRepository
from domain.repositories.task_repository import TaskRepository
from domain.utils.constants import Constants


class GetDashboardUseCase:
    def __init__(self, project_repository: ProjectRepository, task_repository: TaskRepository):
        self.project_repository = project_repository
        self.task_repository = task_repository

    def execute_due_soon_tasks(self, user_id: str, today: date = None) -> List[TaskDueSoon]:
        today = today or date.today()

        return self.task_repository.get_due_soon_tasks(
            user_id=user_id,
            due_from=today,
            due_to=today + timedelta(days=Constants.DASHBOARD_DUE_SOON_DAYS)
        )

    def execute(self, user_id: str, today: date = None) -> DashboardMetrics:
        today = today or date.today()

        window_start, window_end = self._weekly_window(today)

        project_summaries = self.project_repository.get_user_project_summaries(user_id=user_id)

        task_metrics = self.task_repository.get_metrics(
            user_id=user_id,
            due_from=today,
            due_to=today + timedelta(days=Constants.DASHBOARD_DUE_SOON_DAYS)
        )

        weekly_activity = self.task_repository.get_weekly_activity(
            user_id=user_id,
            start_at=window_start,
            end_at=window_end
        )

        return DashboardMetrics(
            total_projects=len(project_summaries),
            projects_by_status=self._count_projects_by_status(project_summaries),
            total_tasks=task_metrics.total_tasks,
            completed_tasks=task_metrics.completed_tasks,
            tasks_due_soon=task_metrics.tasks_due_soon,
            weekly_performance=self._build_weekly_performance(today, weekly_activity)
        )

    def _count_projects_by_status(self, project_summaries: List) -> List[ProjectStatusCount]:
        counts = {
            status: 0
            for status in ProjectStatusEnum
        }

        for summary in project_summaries:
            counts[summary.status] += 1

        return [
            ProjectStatusCount(status=status, total=counts[status])
            for status in ProjectStatusEnum
        ]

    def _weekly_window(self, today: date) -> tuple[datetime, datetime]:
        first_day = today - timedelta(days=Constants.DASHBOARD_WEEKLY_DAYS - 1)

        start_at = datetime.combine(first_day, time.min)
        end_at = datetime.combine(today + timedelta(days=1), time.min)

        return start_at, end_at

    def _build_weekly_performance(self, today: date, activity: List) -> List[WeeklyPerformance]:
        activity_by_day = {item.day: item for item in activity}

        performance = []

        for offset in range(Constants.DASHBOARD_WEEKLY_DAYS):
            day = today - timedelta(days=Constants.DASHBOARD_WEEKLY_DAYS - 1 - offset)

            item = activity_by_day.get(day)

            performance.append(
                WeeklyPerformance(
                    name=Constants.WEEKDAY_SHORT_NAMES[day.weekday()],
                    completed=item.completed if item else 0,
                    created=item.created if item else 0
                )
            )

        return performance
