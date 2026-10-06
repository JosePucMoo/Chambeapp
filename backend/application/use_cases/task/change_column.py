

from domain.exceptions.cannot_update_exception import CannotUpdateException
from domain.exceptions.not_found_exception import NotFoundException
from domain.repositories.column_repository import ColumnRepository
from domain.repositories.task_repository import TaskRepository
from domain.utils.constants import Constants


class ChangeColumnUseCase:
    def __init__(self, repository: TaskRepository, column_repository: ColumnRepository):
        self.repository = repository
        self.column_repository = column_repository

    def execute(self, user_id: str, task_id: str, column_id: str):
        task_detail = self.repository.get_detail_by_id(user_id=user_id, task_id=task_id)

        if not task_detail:
            raise NotFoundException(Constants.TASK_NOT_FOUND)

        target_column = self.column_repository.get_by_id(column_id)

        if not target_column:
            raise NotFoundException(Constants.COLUMN_NOT_FOUND)

        if target_column.project_id != task_detail.project_id:
            raise CannotUpdateException(Constants.TASK_NOT_UPDATED)

        return self.repository.change_column(task_id, column_id)
