from datetime import date

from mockito import verify, when, ANY

import pytest

from application.use_cases.task.change_column import ChangeColumnUseCase
from domain.entities.column import Column
from domain.entities.enums import TaskPriorityEnum
from domain.entities.task import TaskDetail
from domain.exceptions.cannot_update_exception import CannotUpdateException
from domain.exceptions.not_found_exception import NotFoundException
from domain.repositories.column_repository import ColumnRepository
from domain.repositories.task_repository import TaskRepository
from domain.utils.constants import Constants


class TestChangeColumnUseCase:
    @pytest.fixture
    def task_detail(self) -> TaskDetail:
        return TaskDetail(
            id="task-1",
            title="Task",
            description="A description",
            priority=TaskPriorityEnum.HIGH,
            due_date=date(2026, 12, 31),
            column_id="column-1",
            column_title="To Do",
            project_id="project-1",
            project_title="Project",
            assignee_id="user-1",
        )

    def test_change_column_succesfully(
        self,
        change_column_use_case: ChangeColumnUseCase,
        mock_task_repository: TaskRepository,
        mock_column_repository: ColumnRepository,
        task_detail: TaskDetail,
    ):
        column = Column(title="Done", position=2, project_id=task_detail.project_id)
        when(mock_task_repository).get_detail_by_id(
            user_id="user-1", task_id=task_detail.id
        ).thenReturn(task_detail)
        when(mock_column_repository).get_by_id(column.id).thenReturn(column)
        when(mock_task_repository).change_column(task_detail.id, column.id).thenReturn(task_detail)

        result = change_column_use_case.execute("user-1", task_detail.id, column.id)

        assert result == task_detail
        verify(mock_task_repository).get_detail_by_id(user_id="user-1", task_id=task_detail.id)
        verify(mock_column_repository).get_by_id(column.id)
        verify(mock_task_repository).change_column(task_detail.id, column.id)

    def test_task_not_found(
        self,
        change_column_use_case: ChangeColumnUseCase,
        mock_task_repository: TaskRepository,
        mock_column_repository: ColumnRepository,
        task_detail: TaskDetail,
    ):
        when(mock_task_repository).get_detail_by_id(
            user_id="user-1", task_id=task_detail.id
        ).thenReturn(None)

        with pytest.raises(NotFoundException, match=Constants.TASK_NOT_FOUND):
            change_column_use_case.execute("user-1", task_detail.id, "column-2")

        verify(mock_column_repository, times=0).get_by_id(ANY)
        verify(mock_task_repository, times=0).change_column(ANY, ANY)

    def test_column_not_found(
        self,
        change_column_use_case: ChangeColumnUseCase,
        mock_task_repository: TaskRepository,
        mock_column_repository: ColumnRepository,
        task_detail: TaskDetail,
    ):
        when(mock_task_repository).get_detail_by_id(
            user_id="user-1", task_id=task_detail.id
        ).thenReturn(task_detail)
        when(mock_column_repository).get_by_id("column-2").thenReturn(None)

        with pytest.raises(NotFoundException, match=Constants.COLUMN_NOT_FOUND):
            change_column_use_case.execute("user-1", task_detail.id, "column-2")

        verify(mock_task_repository, times=0).change_column(ANY, ANY)

    def test_column_from_another_project(
        self,
        change_column_use_case: ChangeColumnUseCase,
        mock_task_repository: TaskRepository,
        mock_column_repository: ColumnRepository,
        task_detail: TaskDetail,
    ):
        column = Column(title="Done", position=2, project_id="another-project")
        when(mock_task_repository).get_detail_by_id(
            user_id="user-1", task_id=task_detail.id
        ).thenReturn(task_detail)
        when(mock_column_repository).get_by_id(column.id).thenReturn(column)

        with pytest.raises(CannotUpdateException, match=Constants.TASK_NOT_UPDATED):
            change_column_use_case.execute("user-1", task_detail.id, column.id)

        verify(mock_column_repository).get_by_id(column.id)
        verify(mock_task_repository, times=0).change_column(ANY, ANY)
