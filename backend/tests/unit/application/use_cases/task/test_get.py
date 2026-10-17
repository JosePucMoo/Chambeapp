from datetime import date

from mockito import verify, when, ANY

import pytest

from application.use_cases.task.get import GetTaskUseCase
from domain.entities.enums import TaskPriorityEnum
from domain.entities.task import CalendarTask, TaskDetail, TaskFilters
from domain.exceptions.not_found_exception import NotFoundException
from domain.repositories.task_repository import TaskRepository
from domain.utils.constants import Constants


class TestGetTaskUseCase:
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

    def test_execute_paginated_summary(
        self,
        get_task_use_case: GetTaskUseCase,
        mock_task_repository: TaskRepository,
    ):
        expected = (1, ["summary"])
        when(mock_task_repository).get_paginated_dashboard_tasks(
            user_id="user-1", page=1, page_size=10, filters=None
        ).thenReturn(expected)

        result = get_task_use_case.execute_paginated_summary("user-1", 1, 10)

        assert result == expected
        verify(mock_task_repository).get_paginated_dashboard_tasks(
            user_id="user-1", page=1, page_size=10, filters=None
        )

    def test_execute_paginated_summary_with_filters(
        self,
        get_task_use_case: GetTaskUseCase,
        mock_task_repository: TaskRepository,
    ):
        filters = TaskFilters(search="abc")
        when(mock_task_repository).get_paginated_dashboard_tasks(
            user_id="user-1", page=2, page_size=5, filters=filters
        ).thenReturn((0, []))

        result = get_task_use_case.execute_paginated_summary("user-1", 2, 5, filters)

        assert result == (0, [])
        verify(mock_task_repository).get_paginated_dashboard_tasks(
            user_id="user-1", page=2, page_size=5, filters=filters
        )

    def test_execute_calendar(
        self,
        get_task_use_case: GetTaskUseCase,
        mock_task_repository: TaskRepository,
    ):
        start = date(2026, 1, 1)
        end = date(2026, 1, 31)
        calendar_task = CalendarTask(
            id="task-1",
            title="Task",
            description="A description",
            project_id="project-1",
            project_title="Project",
            column_id="column-1",
            column_title="To Do",
            priority=TaskPriorityEnum.HIGH,
            due_date=date(2026, 1, 15),
            assignee_id="user-1",
        )
        when(mock_task_repository).get_calendar_tasks(
            user_id="user-1", start_date=start, end_date=end, filters=None
        ).thenReturn([calendar_task])

        result = get_task_use_case.execute_calendar("user-1", start, end)

        assert result == [calendar_task]
        verify(mock_task_repository).get_calendar_tasks(
            user_id="user-1", start_date=start, end_date=end, filters=None
        )

    def test_execute_detail_succesfully(
        self,
        get_task_use_case: GetTaskUseCase,
        mock_task_repository: TaskRepository,
        task_detail: TaskDetail,
    ):
        when(mock_task_repository).get_detail_by_id(
            user_id="user-1", task_id=task_detail.id
        ).thenReturn(task_detail)

        result = get_task_use_case.execute_detail("user-1", task_detail.id)

        assert result == task_detail
        verify(mock_task_repository).get_detail_by_id(user_id="user-1", task_id=task_detail.id)

    def test_execute_detail_not_found(
        self,
        get_task_use_case: GetTaskUseCase,
        mock_task_repository: TaskRepository,
        task_detail: TaskDetail,
    ):
        when(mock_task_repository).get_detail_by_id(
            user_id="user-1", task_id=task_detail.id
        ).thenReturn(None)

        with pytest.raises(NotFoundException, match=Constants.TASK_NOT_FOUND):
            get_task_use_case.execute_detail("user-1", task_detail.id)

        verify(mock_task_repository).get_detail_by_id(user_id="user-1", task_id=ANY)
