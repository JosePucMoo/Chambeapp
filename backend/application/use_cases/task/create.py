

from domain.repositories.column_repository import ColumnRepository
from domain.exceptions.not_found_exception import NotFoundException
from domain.repositories.project_repository import ProjectRepository
from domain.exceptions.cannot_create_exception import CannotCreateException
from domain.utils.constants import Constants
from domain.entities.task import Task
from domain.repositories.task_repository import TaskRepository


class CreateTaskUseCase:
    def __init__(self, repository: TaskRepository, project_repository: ProjectRepository, column_repository: ColumnRepository):
        self.repository = repository
        self.project_repository = project_repository
        self.column_repository = column_repository

    def execute(self, project_id: str, task_data: Task) -> Task:

        if not self.project_repository.get_by_id(project_id):
            raise NotFoundException(Constants.PROJECT_NOT_FOUND)

        column = self.column_repository.get_the_first_column_by_project(project_id)

        if not column:
            raise NotFoundException(Constants.ANY_COLUMN_FOUND)

        task_data.column_id = column.id

        task = self.repository.create(task_data)

        if not task:
            raise CannotCreateException(Constants.TASK_NOT_CREATED)

        return task