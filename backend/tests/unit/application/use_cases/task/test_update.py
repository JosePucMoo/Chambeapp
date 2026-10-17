from datetime import date, datetime

from mockito import verify, when, ANY

import pytest

from application.use_cases.task.update import UpdateTaskUseCase
from domain.entities.enums import RoleEnum, TaskPriorityEnum
from domain.entities.project import ProjectMember
from domain.entities.task import Task, TaskDetail
from domain.exceptions.cannot_update_exception import CannotUpdateException
from domain.exceptions.not_found_exception import NotFoundException
from domain.repositories.project_repository import ProjectRepository
from domain.repositories.task_repository import TaskRepository
from domain.utils.constants import Constants


class TestUpdateTaskUseCase:
    @pytest.fixture
    def task_data(self) -> Task:
        return Task(
            title="Updated Task",
            description="A description",
            priority=TaskPriorityEnum.HIGH,
            due_date=datetime(2026, 12, 31),
            assignee_id="user-1",
        )

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

    def test_update_succesfully(
        self,
        update_task_use_case: UpdateTaskUseCase,
        mock_task_repository: TaskRepository,
        mock_project_repository: ProjectRepository,
        task_data: Task,
        task_detail: TaskDetail,
    ):
        member = ProjectMember(
            id="user-1", name="Member", email="member@test.com", role=RoleEnum.OWNER
        )
        when(mock_task_repository).get_detail_by_id(
            user_id="user-1", task_id=task_detail.id
        ).thenReturn(task_detail)
        when(mock_project_repository).get_project_members(task_detail.project_id).thenReturn([member])
        when(mock_task_repository).update(user_id="user-1", task=task_data).thenReturn(task_data)

        result = update_task_use_case.execute("user-1", task_detail.id, task_data)

        assert result == task_data
        verify(mock_task_repository).get_detail_by_id(user_id="user-1", task_id=task_detail.id)
        verify(mock_project_repository).get_project_members(task_detail.project_id)
        verify(mock_task_repository).update(user_id="user-1", task=task_data)

    def test_task_not_found(
        self,
        update_task_use_case: UpdateTaskUseCase,
        mock_task_repository: TaskRepository,
        mock_project_repository: ProjectRepository,
        task_data: Task,
        task_detail: TaskDetail,
    ):
        when(mock_task_repository).get_detail_by_id(
            user_id="user-1", task_id=task_detail.id
        ).thenReturn(None)

        with pytest.raises(NotFoundException, match=Constants.TASK_NOT_FOUND):
            update_task_use_case.execute("user-1", task_detail.id, task_data)

        verify(mock_project_repository, times=0).get_project_members(ANY)
        verify(mock_task_repository, times=0).update(user_id=ANY, task=ANY)

    def test_assignee_not_in_project(
        self,
        update_task_use_case: UpdateTaskUseCase,
        mock_task_repository: TaskRepository,
        mock_project_repository: ProjectRepository,
        task_data: Task,
        task_detail: TaskDetail,
    ):
        member = ProjectMember(
            id="other-user", name="Member", email="member@test.com", role=RoleEnum.OWNER
        )
        when(mock_task_repository).get_detail_by_id(
            user_id="user-1", task_id=task_detail.id
        ).thenReturn(task_detail)
        when(mock_project_repository).get_project_members(task_detail.project_id).thenReturn([member])

        with pytest.raises(CannotUpdateException, match=Constants.ASSIGNEE_NOT_IN_PROJECT):
            update_task_use_case.execute("user-1", task_detail.id, task_data)

        verify(mock_task_repository, times=0).update(user_id=ANY, task=ANY)

    def test_cannot_update_task(
        self,
        update_task_use_case: UpdateTaskUseCase,
        mock_task_repository: TaskRepository,
        mock_project_repository: ProjectRepository,
        task_data: Task,
        task_detail: TaskDetail,
    ):
        member = ProjectMember(
            id="user-1", name="Member", email="member@test.com", role=RoleEnum.OWNER
        )
        when(mock_task_repository).get_detail_by_id(
            user_id="user-1", task_id=task_detail.id
        ).thenReturn(task_detail)
        when(mock_project_repository).get_project_members(task_detail.project_id).thenReturn([member])
        when(mock_task_repository).update(user_id="user-1", task=task_data).thenReturn(None)

        with pytest.raises(CannotUpdateException, match=Constants.TASK_NOT_UPDATED):
            update_task_use_case.execute("user-1", task_detail.id, task_data)

        verify(mock_task_repository).update(user_id="user-1", task=task_data)
