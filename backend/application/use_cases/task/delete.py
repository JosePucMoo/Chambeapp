from typing import List

from domain.exceptions.not_found_exception import NotFoundException
from domain.repositories.task_repository import TaskRepository
from domain.utils.constants import Constants


class DeleteTaskUseCase:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def execute(self, user_id: str, task_id: str) -> None:
        deleted = self.repository.delete(user_id=user_id, task_id=task_id)

        if not deleted:
            raise NotFoundException(Constants.TASK_NOT_FOUND)

    def execute_many(self, user_id: str, task_ids: List[str]) -> List[str]:
        return self.repository.delete_many(user_id=user_id, task_ids=task_ids)