from domain.entities.user_project_link import UserProjectLink
from domain.entities.column import Column
from domain.entities.enums import ColumnDefaultEnum, RoleEnum
from domain.repositories.column_repository import ColumnRepository
from domain.exceptions.cannot_create_exception import CannotCreateException
from domain.utils.constants import Constants
from domain.entities.project import Project
from domain.repositories.project_repository import ProjectRepository
from domain.repositories.user_project_link_repository import UserProjectLinkRepository


class CreateProjectUseCase:
    def __init__(self, repository: ProjectRepository, column_repository: ColumnRepository, user_project_link_repository: UserProjectLinkRepository):
        self.repository=repository
        self.column_repository = column_repository
        self.user_project_link_repository = user_project_link_repository

    def execute(self, project_data, user_id: str)-> Project:
        project = self.repository.create(project_data)

        if not project:
            raise CannotCreateException(Constants.PROJECT_NOT_CREATED)

        column_to_do = Column(
            title=ColumnDefaultEnum.to_do,
            position=1,
            project_id=project.id
        )

        column_in_progress = Column(
            title=ColumnDefaultEnum.in_progress,
            position=2,
            project_id=project.id
        )

        column_completed = Column(
            title=ColumnDefaultEnum.completed,
            position=3,
            project_id=project.id
        )

        default_columns = [
            column_to_do,
            column_in_progress,
            column_completed
        ]

        self.column_repository.create_default_columns(default_columns)

        user_project_link = UserProjectLink(
            role=RoleEnum.owner,
            user_id=user_id,
            project_id=project.id,
        )

        self.user_project_link_repository.create(user_project_link)
        
        return project