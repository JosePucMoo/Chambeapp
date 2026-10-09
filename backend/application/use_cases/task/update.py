from domain.entities.task import Task
from domain.exceptions.cannot_update_exception import CannotUpdateException
from domain.exceptions.not_found_exception import NotFoundException
from domain.repositories.project_repository import ProjectRepository
from domain.repositories.task_repository import TaskRepository
from domain.utils.constants import Constants


class UpdateTaskUseCase:
    def __init__(self, repository: TaskRepository, project_repository: ProjectRepository):
        self.repository = repository
        self.project_repository = project_repository

    def execute(self, user_id: str, task_id: str, task_data: Task) -> Task:
        task_detail = self.repository.get_detail_by_id(user_id=user_id, task_id=task_id)

        if not task_detail:
            raise NotFoundException(Constants.TASK_NOT_FOUND)

        members = self.project_repository.get_project_members(task_detail.project_id)

        if not any(member.id == task_data.assignee_id for member in members):
            raise CannotUpdateException(Constants.ASSIGNEE_NOT_IN_PROJECT)

        updated_task = self.repository.update(user_id=user_id, task=task_data)

        if not updated_task:
            raise CannotUpdateException(Constants.TASK_NOT_UPDATED)

        return updated_task
