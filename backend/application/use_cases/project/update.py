from domain.entities.enums import RoleEnum
from domain.entities.project import Project
from domain.exceptions.cannot_update_exception import CannotUpdateException
from domain.exceptions.forbidden_exception import ForbiddenException
from domain.exceptions.not_found_exception import NotFoundException
from domain.repositories.project_repository import ProjectRepository
from domain.utils.constants import Constants


class UpdateProjectUseCase:
    def __init__(self, repository: ProjectRepository):
        self.repository = repository

    def execute(self, user_id: str, project_data: Project) -> Project:
        current_project = self.repository.get_by_id(project_data.id)

        if not current_project:
            raise NotFoundException(Constants.PROJECT_NOT_FOUND)

        members = self.repository.get_project_members(project_data.id)

        if not any(str(member.id) == str(user_id) for member in members):
            raise ForbiddenException(Constants.PROJECT_FORBIDDEN)

        if not any(
            str(member.id) == str(user_id) and member.role == RoleEnum.OWNER for member in members
        ):
            raise ForbiddenException(Constants.UNAUTHORIZED_ACCESS)

        updated_project = self.repository.update(project_data)

        if not updated_project:
            raise CannotUpdateException(Constants.PROJECT_NOT_UPDATED)

        return updated_project
