from mockito import mock
import pytest

from application.use_cases.task.change_column import ChangeColumnUseCase
from application.use_cases.task.create import CreateTaskUseCase
from application.use_cases.task.delete import DeleteTaskUseCase
from application.use_cases.task.get import GetTaskUseCase
from application.use_cases.task.update import UpdateTaskUseCase
from domain.repositories.column_repository import ColumnRepository
from domain.repositories.project_repository import ProjectRepository
from domain.repositories.task_repository import TaskRepository


@pytest.fixture
def mock_task_repository() -> TaskRepository:
    return mock(TaskRepository)


@pytest.fixture
def mock_project_repository() -> ProjectRepository:
    return mock(ProjectRepository)


@pytest.fixture
def mock_column_repository() -> ColumnRepository:
    return mock(ColumnRepository)


@pytest.fixture
def create_task_use_case(
    mock_task_repository: TaskRepository,
    mock_project_repository: ProjectRepository,
    mock_column_repository: ColumnRepository,
) -> CreateTaskUseCase:
    return CreateTaskUseCase(
        repository=mock_task_repository,
        project_repository=mock_project_repository,
        column_repository=mock_column_repository,
    )


@pytest.fixture
def update_task_use_case(
    mock_task_repository: TaskRepository,
    mock_project_repository: ProjectRepository,
) -> UpdateTaskUseCase:
    return UpdateTaskUseCase(
        repository=mock_task_repository,
        project_repository=mock_project_repository,
    )


@pytest.fixture
def change_column_use_case(
    mock_task_repository: TaskRepository,
    mock_column_repository: ColumnRepository,
) -> ChangeColumnUseCase:
    return ChangeColumnUseCase(
        repository=mock_task_repository,
        column_repository=mock_column_repository,
    )


@pytest.fixture
def delete_task_use_case(mock_task_repository: TaskRepository) -> DeleteTaskUseCase:
    return DeleteTaskUseCase(repository=mock_task_repository)


@pytest.fixture
def get_task_use_case(mock_task_repository: TaskRepository) -> GetTaskUseCase:
    return GetTaskUseCase(repository=mock_task_repository)
