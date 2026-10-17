from datetime import datetime

from mockito import verify, when, ANY

import pytest

from application.use_cases.task.create import CreateTaskUseCase
from domain.entities.column import Column
from domain.entities.enums import TaskPriorityEnum
from domain.entities.project import Project
from domain.entities.task import Task
from domain.exceptions.cannot_create_exception import CannotCreateException
from domain.exceptions.not_found_exception import NotFoundException
from domain.repositories.column_repository import ColumnRepository
from domain.repositories.project_repository import ProjectRepository
from domain.repositories.task_repository import TaskRepository
from domain.utils.constants import Constants


class TestCreateTaskUseCase:
    @pytest.fixture
    def project(self) -> Project:
        return Project(
            title="Project",
            description="A description",
            client="Client",
            delivery_date="2026-12-31",
        )

    @pytest.fixture
    def column(self) -> Column:
        return Column(title="To Do", position=1, project_id="project-1")

    @pytest.fixture
    def task_data(self) -> Task:
        return Task(
            title="New Task",
            description="A description",
            priority=TaskPriorityEnum.HIGH,
            due_date=datetime(2026, 12, 31),
            assignee_id="user-1",
        )

    def test_create_task_succesfully(
        self,
        create_task_use_case: CreateTaskUseCase,
        mock_task_repository: TaskRepository,
        mock_project_repository: ProjectRepository,
        mock_column_repository: ColumnRepository,
        project: Project,
        column: Column,
        task_data: Task,
    ):
        when(mock_project_repository).get_by_id(project.id).thenReturn(project)
        when(mock_column_repository).get_the_first_column_by_project(project.id).thenReturn(column)
        when(mock_task_repository).create(task_data).thenReturn(task_data)

        result = create_task_use_case.execute(project.id, task_data)

        assert result == task_data
        assert task_data.column_id == column.id

        verify(mock_project_repository).get_by_id(project.id)
        verify(mock_column_repository).get_the_first_column_by_project(project.id)
        verify(mock_task_repository).create(task_data)

    def test_project_not_found(
        self,
        create_task_use_case: CreateTaskUseCase,
        mock_task_repository: TaskRepository,
        mock_project_repository: ProjectRepository,
        mock_column_repository: ColumnRepository,
        project: Project,
        task_data: Task,
    ):
        when(mock_project_repository).get_by_id(project.id).thenReturn(None)

        with pytest.raises(NotFoundException, match=Constants.PROJECT_NOT_FOUND):
            create_task_use_case.execute(project.id, task_data)

        verify(mock_column_repository, times=0).get_the_first_column_by_project(ANY)
        verify(mock_task_repository, times=0).create(ANY(Task))

    def test_column_not_found(
        self,
        create_task_use_case: CreateTaskUseCase,
        mock_task_repository: TaskRepository,
        mock_project_repository: ProjectRepository,
        mock_column_repository: ColumnRepository,
        project: Project,
        task_data: Task,
    ):
        when(mock_project_repository).get_by_id(project.id).thenReturn(project)
        when(mock_column_repository).get_the_first_column_by_project(project.id).thenReturn(None)

        with pytest.raises(NotFoundException, match=Constants.ANY_COLUMN_FOUND):
            create_task_use_case.execute(project.id, task_data)

        verify(mock_task_repository, times=0).create(ANY(Task))

    def test_cannot_create_task(
        self,
        create_task_use_case: CreateTaskUseCase,
        mock_task_repository: TaskRepository,
        mock_project_repository: ProjectRepository,
        mock_column_repository: ColumnRepository,
        project: Project,
        column: Column,
        task_data: Task,
    ):
        when(mock_project_repository).get_by_id(project.id).thenReturn(project)
        when(mock_column_repository).get_the_first_column_by_project(project.id).thenReturn(column)
        when(mock_task_repository).create(task_data).thenReturn(None)

        with pytest.raises(CannotCreateException, match=Constants.TASK_NOT_CREATED):
            create_task_use_case.execute(project.id, task_data)

        verify(mock_task_repository).create(task_data)
