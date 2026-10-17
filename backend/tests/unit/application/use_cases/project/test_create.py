from mockito import verify, when, ANY

import pytest

from application.use_cases.project.create import CreateProjectUseCase
from domain.entities.column import Column
from domain.entities.enums import ColumnDefaultEnum, RoleEnum
from domain.entities.project import Project
from domain.entities.user_project_link import UserProjectLink
from domain.exceptions.cannot_create_exception import CannotCreateException
from domain.repositories.column_repository import ColumnRepository
from domain.repositories.project_repository import ProjectRepository
from domain.repositories.user_project_link_repository import UserProjectLinkRepository
from domain.utils.constants import Constants


class TestCreateProjectUseCase:
    @pytest.fixture
    def project_data(self) -> Project:
        return Project(
            title="New Project",
            description="A description",
            client="Client",
            delivery_date="2026-12-31",
        )

    @pytest.fixture
    def user_id(self) -> str:
        return "user-123"

    def test_create_project_succesfully(
        self,
        create_project_use_case: CreateProjectUseCase,
        mock_project_repository: ProjectRepository,
        mock_column_repository: ColumnRepository,
        mock_user_project_link_repository: UserProjectLinkRepository,
        project_data: Project,
        user_id: str,
    ):
        when(mock_project_repository).create(project_data).thenReturn(project_data)

        captured_columns = {}
        when(mock_column_repository).create_default_columns(ANY(list)).thenAnswer(
            lambda columns: captured_columns.setdefault("value", columns)
        )

        captured_link = {}
        when(mock_user_project_link_repository).create(ANY(UserProjectLink)).thenAnswer(
            lambda link: captured_link.setdefault("value", link)
        )

        result = create_project_use_case.execute(project_data, user_id)

        assert result == project_data

        columns = captured_columns["value"]
        assert len(columns) == 3
        assert [column.title for column in columns] == [
            ColumnDefaultEnum.TO_DO,
            ColumnDefaultEnum.IN_PROGRESS,
            ColumnDefaultEnum.COMPLETED,
        ]
        assert [column.position for column in columns] == [1, 2, 3]
        assert all(column.project_id == project_data.id for column in columns)

        link = captured_link["value"]
        assert isinstance(link, UserProjectLink)
        assert link.role == RoleEnum.OWNER
        assert link.user_id == user_id
        assert link.project_id == project_data.id

        verify(mock_project_repository).create(project_data)
        verify(mock_column_repository).create_default_columns(ANY(list))
        verify(mock_user_project_link_repository).create(ANY(UserProjectLink))

    def test_cannot_create_project(
        self,
        create_project_use_case: CreateProjectUseCase,
        mock_project_repository: ProjectRepository,
        mock_column_repository: ColumnRepository,
        mock_user_project_link_repository: UserProjectLinkRepository,
        project_data: Project,
        user_id: str,
    ):
        when(mock_project_repository).create(project_data).thenReturn(None)

        with pytest.raises(CannotCreateException, match=Constants.PROJECT_NOT_CREATED):
            create_project_use_case.execute(project_data, user_id)

        verify(mock_project_repository).create(project_data)
        verify(mock_column_repository, times=0).create_default_columns(ANY(list))
        verify(mock_user_project_link_repository, times=0).create(ANY(UserProjectLink))

    def test_default_columns_are_created(
        self,
        create_project_use_case: CreateProjectUseCase,
        mock_project_repository: ProjectRepository,
        mock_column_repository: ColumnRepository,
        mock_user_project_link_repository: UserProjectLinkRepository,
        project_data: Project,
        user_id: str,
    ):
        captured = {}
        when(mock_project_repository).create(project_data).thenReturn(project_data)
        when(mock_column_repository).create_default_columns(ANY(list)).thenAnswer(
            lambda columns: captured.setdefault("columns", columns)
        )
        when(mock_user_project_link_repository).create(ANY(UserProjectLink)).thenReturn(None)

        create_project_use_case.execute(project_data, user_id)

        assert all(isinstance(column, Column) for column in captured["columns"])
