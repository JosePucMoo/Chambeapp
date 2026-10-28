from datetime import date, datetime, time, timedelta
from types import SimpleNamespace

from mockito import verify, when, ANY

from application.use_cases.dashboard.get import GetDashboardUseCase
from domain.entities.dashboard import ProjectStatusCount, WeeklyPerformance
from domain.entities.enums import ProjectStatusEnum, TaskPriorityEnum
from domain.entities.task import DailyTaskActivity, TaskDashboardSummary, TaskMetricsAggregate
from domain.repositories.project_repository import ProjectRepository
from domain.repositories.task_repository import TaskRepository
from domain.utils.constants import Constants


TODAY = datetime.now()


def _summary(status: ProjectStatusEnum) -> SimpleNamespace:
    return SimpleNamespace(status=status)


class TestGetDashboardUseCase:
    def test_execute_due_soon_tasks(
        self,
        get_dashboard_use_case: GetDashboardUseCase,
        mock_task_repository: TaskRepository,
    ):
        due_soon = [
            TaskDashboardSummary(
                id="task-1",
                title="Task",
                project_title="Project",
                priority=TaskPriorityEnum.HIGH,
                due_date=TODAY,
                column_title="To Do",
                project_id="project_id",
            )
        ]
        when(mock_task_repository).get_due_soon_tasks(
            user_id="user-1",
            due_from=TODAY,
            due_to=TODAY + timedelta(days=Constants.DASHBOARD_DUE_SOON_DAYS),
        ).thenReturn(due_soon)

        result = get_dashboard_use_case.execute_due_soon_tasks("user-1", today=TODAY)

        assert result == due_soon
        verify(mock_task_repository).get_due_soon_tasks(
            user_id="user-1",
            due_from=TODAY,
            due_to=TODAY + timedelta(days=Constants.DASHBOARD_DUE_SOON_DAYS),
        )

    def test_execute_due_soon_defaults_to_today(
        self,
        get_dashboard_use_case: GetDashboardUseCase,
        mock_task_repository: TaskRepository,
    ):
        when(mock_task_repository).get_due_soon_tasks(
            user_id="user-1", due_from=ANY(date), due_to=ANY(date)
        ).thenReturn([])

        result = get_dashboard_use_case.execute_due_soon_tasks("user-1")

        assert result == []

    def test_execute_aggregates_metrics(
        self,
        get_dashboard_use_case: GetDashboardUseCase,
        mock_project_repository: ProjectRepository,
        mock_task_repository: TaskRepository,
    ):
        summaries = [
            _summary(ProjectStatusEnum.ACTIVE),
            _summary(ProjectStatusEnum.ACTIVE),
            _summary(ProjectStatusEnum.COMPLETED),
        ]
        metrics = TaskMetricsAggregate(total_tasks=10, completed_tasks=4, tasks_due_soon=2)
        activity = [DailyTaskActivity(day=TODAY, completed=3, created=5)]

        when(mock_project_repository).get_user_project_summaries(user_id="user-1").thenReturn(
            summaries
        )
        when(mock_task_repository).get_metrics(
            user_id="user-1",
            due_from=TODAY,
            due_to=TODAY + timedelta(days=Constants.DASHBOARD_DUE_SOON_DAYS),
        ).thenReturn(metrics)
        window_start, window_end = get_dashboard_use_case._weekly_window(TODAY)
        when(mock_task_repository).get_weekly_activity(
            user_id="user-1", start_at=window_start, end_at=window_end
        ).thenReturn(activity)

        result = get_dashboard_use_case.execute("user-1", today=TODAY)

        assert result.total_projects == 3
        assert result.total_tasks == 10
        assert result.completed_tasks == 4
        assert result.tasks_due_soon == 2
        assert len(result.weekly_performance) == Constants.DASHBOARD_WEEKLY_DAYS

        by_status = {entry.status: entry.total for entry in result.projects_by_status}
        assert by_status[ProjectStatusEnum.ACTIVE] == 2
        assert by_status[ProjectStatusEnum.COMPLETED] == 1
        assert by_status[ProjectStatusEnum.NOT_STARTED] == 0
        assert by_status[ProjectStatusEnum.DELAYED] == 0

        assert result.weekly_performance[-1] == WeeklyPerformance(
            name=Constants.WEEKDAY_SHORT_NAMES[TODAY.weekday()], completed=3, created=5
        )

        verify(mock_project_repository).get_user_project_summaries(user_id="user-1")
        verify(mock_task_repository).get_metrics(
            user_id="user-1",
            due_from=TODAY,
            due_to=TODAY + timedelta(days=Constants.DASHBOARD_DUE_SOON_DAYS),
        )
        verify(mock_task_repository).get_weekly_activity(
            user_id="user-1", start_at=window_start, end_at=window_end
        )

    def test_count_projects_by_status(
        self,
        get_dashboard_use_case: GetDashboardUseCase,
    ):
        summaries = [
            _summary(ProjectStatusEnum.ACTIVE),
            _summary(ProjectStatusEnum.COMPLETED),
            _summary(ProjectStatusEnum.COMPLETED),
        ]

        result = get_dashboard_use_case._count_projects_by_status(summaries)

        assert len(result) == len(ProjectStatusEnum)
        assert all(isinstance(entry, ProjectStatusCount) for entry in result)
        by_status = {entry.status: entry.total for entry in result}
        assert by_status[ProjectStatusEnum.ACTIVE] == 1
        assert by_status[ProjectStatusEnum.COMPLETED] == 2
        assert by_status[ProjectStatusEnum.NOT_STARTED] == 0
        assert by_status[ProjectStatusEnum.DELAYED] == 0

    def test_weekly_window(self, get_dashboard_use_case: GetDashboardUseCase):
        start, end = get_dashboard_use_case._weekly_window(TODAY)

        assert start == datetime.combine(TODAY - timedelta(days=6), time.min)
        assert end == datetime.combine(TODAY + timedelta(days=1), time.min)
        assert (end - start).days == Constants.DASHBOARD_WEEKLY_DAYS

    def test_build_weekly_performance_with_activity(
        self,
        get_dashboard_use_case: GetDashboardUseCase,
    ):
        activity = [DailyTaskActivity(day=TODAY, completed=3, created=5)]

        result = get_dashboard_use_case._build_weekly_performance(TODAY, activity)

        assert len(result) == Constants.DASHBOARD_WEEKLY_DAYS
        assert result[-1] == WeeklyPerformance(
            name=Constants.WEEKDAY_SHORT_NAMES[TODAY.weekday()], completed=3, created=5
        )
        assert result[0].completed == 0
        assert result[0].created == 0

    def test_build_weekly_performance_fills_zeros_for_missing_days(
        self,
        get_dashboard_use_case: GetDashboardUseCase,
    ):
        result = get_dashboard_use_case._build_weekly_performance(TODAY, [])

        assert len(result) == Constants.DASHBOARD_WEEKLY_DAYS
        assert all(entry.completed == 0 for entry in result)
        assert all(entry.created == 0 for entry in result)
        assert result[-1].name == Constants.WEEKDAY_SHORT_NAMES[TODAY.weekday()]
