from datetime import datetime, timedelta
import uuid

import pytest

from domain.entities.enums import ProjectStatusEnum, RoleEnum
from domain.entities.project import ProjectDashboardSummary


class TestProject:
    def test_dashboard_progress_calculate_with_tasks(self):
        total_tasks = 10
        completed_tasks = 3
        progress_expect = (completed_tasks / total_tasks) * 100.0
        delivery_date = (datetime.now() + timedelta(days=5)).date()

        project_dashboard = ProjectDashboardSummary(
            id=uuid.uuid4(),
            title="TestProjectDashboardSummary",
            client="TesClient",
            role=RoleEnum.OWNER,
            delivery_date=delivery_date,
            total_tasks=total_tasks,
            completed_tasks=completed_tasks,
            not_started_tasks=6,
        )

        assert project_dashboard.progress_percentage == pytest.approx(progress_expect)

    def test_dashboard_progress_calculate_with_zero_tasks(self):
        total_tasks = 0
        completed_tasks = 0
        progress_expect = 0
        delivery_date = (datetime.now() + timedelta(days=5)).date()
        not_started_tasks = 6

        project_dashboard = ProjectDashboardSummary(
            id=uuid.uuid4(),
            title="TestProjectDashboardSummary",
            client="TesClient",
            role=RoleEnum.OWNER,
            delivery_date=delivery_date,
            total_tasks=total_tasks,
            completed_tasks=completed_tasks,
            not_started_tasks=not_started_tasks,
        )

        assert project_dashboard.progress_percentage == progress_expect

    def test_dashboard_status_delayed(self):
        total_tasks = 10
        completed_tasks = 5
        progress_expect = (completed_tasks / total_tasks) * 100.0
        delivery_date = (datetime.now() - timedelta(days=5)).date()
        not_started_tasks = 3

        project_dashboard = ProjectDashboardSummary(
            id=uuid.uuid4(),
            title="TestProjectDashboardSummary",
            client="TesClient",
            role=RoleEnum.OWNER,
            delivery_date=delivery_date,
            total_tasks=total_tasks,
            completed_tasks=completed_tasks,
            not_started_tasks=not_started_tasks,
        )

        assert project_dashboard.progress_percentage == pytest.approx(progress_expect)
        assert project_dashboard.status == ProjectStatusEnum.DELAYED

    def test_dashboard_status_not_started_no_tasks(self):
        total_tasks = 0
        completed_tasks = 0
        progress_expect = 0
        delivery_date = (datetime.now() - timedelta(days=5)).date()
        not_started_tasks = 0

        project_dashboard = ProjectDashboardSummary(
            id=uuid.uuid4(),
            title="TestProjectDashboardSummary",
            client="TesClient",
            role=RoleEnum.OWNER,
            delivery_date=delivery_date,
            total_tasks=total_tasks,
            completed_tasks=completed_tasks,
            not_started_tasks=not_started_tasks,
        )

        assert project_dashboard.progress_percentage == pytest.approx(progress_expect)
        assert project_dashboard.status == ProjectStatusEnum.NOT_STARTED

    def test_dashboard_status_completed_all_done(self):
        total_tasks = 10
        completed_tasks = 10
        progress_expect = 100
        delivery_date = (datetime.now() - timedelta(days=5)).date()
        not_started_tasks = 0

        project_dashboard = ProjectDashboardSummary(
            id=uuid.uuid4(),
            title="TestProjectDashboardSummary",
            client="TesClient",
            role=RoleEnum.OWNER,
            delivery_date=delivery_date,
            total_tasks=total_tasks,
            completed_tasks=completed_tasks,
            not_started_tasks=not_started_tasks,
        )

        assert project_dashboard.progress_percentage == pytest.approx(progress_expect)
        assert project_dashboard.status == ProjectStatusEnum.COMPLETED

    def test_dashboard_status_not_started_all_not_started(self):
        total_tasks = 10
        completed_tasks = 0
        progress_expect = 0
        delivery_date = (datetime.now() + timedelta(days=5)).date()
        not_started_tasks = 10

        project_dashboard = ProjectDashboardSummary(
            id=uuid.uuid4(),
            title="TestProjectDashboardSummary",
            client="TesClient",
            role=RoleEnum.OWNER,
            delivery_date=delivery_date,
            total_tasks=total_tasks,
            completed_tasks=completed_tasks,
            not_started_tasks=not_started_tasks,
        )

        assert project_dashboard.progress_percentage == pytest.approx(progress_expect)
        assert project_dashboard.status == ProjectStatusEnum.NOT_STARTED

    def test_dashboard_status_active_mixed(self):
        total_tasks = 10
        completed_tasks = 7
        progress_expect = (completed_tasks / total_tasks) * 100.0
        delivery_date = (datetime.now() + timedelta(days=5)).date()
        not_started_tasks = 2

        project_dashboard = ProjectDashboardSummary(
            id=uuid.uuid4(),
            title="TestProjectDashboardSummary",
            client="TesClient",
            role=RoleEnum.OWNER,
            delivery_date=delivery_date,
            total_tasks=total_tasks,
            completed_tasks=completed_tasks,
            not_started_tasks=not_started_tasks,
        )

        assert project_dashboard.progress_percentage == pytest.approx(progress_expect)
        assert project_dashboard.status == ProjectStatusEnum.ACTIVE
