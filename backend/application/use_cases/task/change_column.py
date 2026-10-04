

from domain.exceptions.not_found_exception import NotFoundException
from domain.repositories.column_repository import ColumnRepository
from domain.repositories.task_repository import TaskRepository
from domain.utils.constants import Constants


class ChangeColumnUseCase:
    def __init__(self, repository: TaskRepository, column_repository: ColumnRepository):
        self.repositoy = repository
        self.column_repository = column_repository


    def execute(self, task_id: str, column_id: str):
        task = self.repositoy.get_by_id(task_id)

        if not task:
            raise NotFoundException(Constants.TASK_NOT_FOUND)

        if not self.column_repository.get_by_id(column_id):
            raise NotFoundException(Constants.COLUMN_NOT_FOUND)

        task = self.repositoy.change_column(task_id, column_id)

        return task