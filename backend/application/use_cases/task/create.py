

from domain.exceptions.cannot_create_exception import CannotCreateException
from domain.utils.constants import Constants
from domain.entities.task import Task
from domain.repositories.task_repository import TaskRepository


class CreateTaskUseCase:
    def __init__(self, repository: TaskRepository):
        self. repository = repository

    def execute(self, task_data: Task) -> Task:
        task = self.repository.create(task_data)

        if not task:
            raise CannotCreateException(Constants.TASK_NOT_CREATED)

        return task