from mockito import mock
import pytest

from application.use_cases.dashboard.get import GetDashboardUseCase
from domain.repositories.project_repository import ProjectRepository
from domain.repositories.task_repository import TaskRepository


@pytest.fixture
def mock_project_repository() -> ProjectRepository:
    return mock(ProjectRepository)


@pytest.fixture
def mock_task_repository() -> TaskRepository:
    return mock(TaskRepository)


@pytest.fixture
def get_dashboard_use_case(
    mock_project_repository: ProjectRepository,
    mock_task_repository: TaskRepository,
) -> GetDashboardUseCase:
    return GetDashboardUseCase(
        project_repository=mock_project_repository,
        task_repository=mock_task_repository,
    )
