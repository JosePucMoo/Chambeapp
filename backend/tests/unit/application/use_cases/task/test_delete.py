from mockito import verify, when, ANY

import pytest

from application.use_cases.task.delete import DeleteTaskUseCase
from domain.exceptions.not_found_exception import NotFoundException
from domain.repositories.task_repository import TaskRepository
from domain.utils.constants import Constants


class TestDeleteTaskUseCase:
    def test_delete_succesfully(
        self,
        delete_task_use_case: DeleteTaskUseCase,
        mock_task_repository: TaskRepository,
    ):
        when(mock_task_repository).delete(user_id="user-1", task_id="task-1").thenReturn(True)

        response = delete_task_use_case.execute("user-1", "task-1")

        assert response is None
        verify(mock_task_repository).delete(user_id="user-1", task_id="task-1")

    def test_delete_task_not_found(
        self,
        delete_task_use_case: DeleteTaskUseCase,
        mock_task_repository: TaskRepository,
    ):
        when(mock_task_repository).delete(user_id="user-1", task_id="task-1").thenReturn(False)

        with pytest.raises(NotFoundException, match=Constants.TASK_NOT_FOUND):
            delete_task_use_case.execute("user-1", "task-1")

        verify(mock_task_repository).delete(user_id="user-1", task_id="task-1")

    def test_execute_many_returns_deleted_ids(
        self,
        delete_task_use_case: DeleteTaskUseCase,
        mock_task_repository: TaskRepository,
    ):
        task_ids = ["task-1", "task-2"]
        when(mock_task_repository).delete_many(user_id="user-1", task_ids=task_ids).thenReturn(
            ["task-1"]
        )

        result = delete_task_use_case.execute_many("user-1", task_ids)

        assert result == ["task-1"]
        verify(mock_task_repository).delete_many(user_id="user-1", task_ids=task_ids)

    def test_execute_many_with_empty_result(
        self,
        delete_task_use_case: DeleteTaskUseCase,
        mock_task_repository: TaskRepository,
    ):
        task_ids = ["task-1"]
        when(mock_task_repository).delete_many(user_id="user-1", task_ids=task_ids).thenReturn([])

        result = delete_task_use_case.execute_many("user-1", task_ids)

        assert result == []
        verify(mock_task_repository).delete_many(user_id="user-1", task_ids=ANY)
