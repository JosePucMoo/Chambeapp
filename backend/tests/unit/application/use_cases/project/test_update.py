from mockito import verify, when, ANY

import pytest

from application.use_cases.project.update import UpdateProjectUseCase
from domain.entities.enums import RoleEnum
from domain.entities.project import Project, ProjectMember
from domain.exceptions.cannot_update_exception import CannotUpdateException
from domain.exceptions.forbidden_exception import ForbiddenException
from domain.exceptions.not_found_exception import NotFoundException
from domain.repositories.project_repository import ProjectRepository
from domain.utils.constants import Constants


class TestUpdateProjectUseCase:
    @pytest.fixture
    def project_data(self) -> Project:
        return Project(
            title="Updated Project",
            description="A description",
            client="Client",
            delivery_date="2026-12-31",
        )

    def test_update_succesfully(
        self,
        update_project_use_case: UpdateProjectUseCase,
        mock_project_repository: ProjectRepository,
        project_data: Project,
    ):
        member = ProjectMember(
            id="user-1", name="Owner", email="owner@test.com", role=RoleEnum.OWNER
        )
        when(mock_project_repository).get_by_id(project_data.id).thenReturn(project_data)
        when(mock_project_repository).get_project_members(project_data.id).thenReturn([member])
        when(mock_project_repository).update(project_data).thenReturn(project_data)

        result = update_project_use_case.execute("user-1", project_data)

        assert result == project_data
        verify(mock_project_repository).get_by_id(project_data.id)
        verify(mock_project_repository).get_project_members(project_data.id)
        verify(mock_project_repository).update(project_data)

    def test_project_not_found(
        self,
        update_project_use_case: UpdateProjectUseCase,
        mock_project_repository: ProjectRepository,
        project_data: Project,
    ):
        when(mock_project_repository).get_by_id(project_data.id).thenReturn(None)

        with pytest.raises(NotFoundException, match=Constants.PROJECT_NOT_FOUND):
            update_project_use_case.execute("user-1", project_data)

        verify(mock_project_repository).get_by_id(project_data.id)
        verify(mock_project_repository, times=0).update(ANY(Project))

    def test_user_is_not_member(
        self,
        update_project_use_case: UpdateProjectUseCase,
        mock_project_repository: ProjectRepository,
        project_data: Project,
    ):
        member = ProjectMember(
            id="other-user", name="Other", email="other@test.com", role=RoleEnum.OWNER
        )
        when(mock_project_repository).get_by_id(project_data.id).thenReturn(project_data)
        when(mock_project_repository).get_project_members(project_data.id).thenReturn([member])

        with pytest.raises(ForbiddenException, match=Constants.PROJECT_FORBIDDEN):
            update_project_use_case.execute("user-1", project_data)

        verify(mock_project_repository).get_project_members(project_data.id)
        verify(mock_project_repository, times=0).update(ANY(Project))

    def test_member_is_not_owner(
        self,
        update_project_use_case: UpdateProjectUseCase,
        mock_project_repository: ProjectRepository,
        project_data: Project,
    ):
        member = ProjectMember(
            id="user-1", name="Guest", email="guest@test.com", role=RoleEnum.GUEST
        )
        when(mock_project_repository).get_by_id(project_data.id).thenReturn(project_data)
        when(mock_project_repository).get_project_members(project_data.id).thenReturn([member])

        with pytest.raises(ForbiddenException, match=Constants.UNAUTHORIZED_ACCESS):
            update_project_use_case.execute("user-1", project_data)

        verify(mock_project_repository).get_project_members(project_data.id)
        verify(mock_project_repository, times=0).update(ANY(Project))

    def test_cannot_update_project(
        self,
        update_project_use_case: UpdateProjectUseCase,
        mock_project_repository: ProjectRepository,
        project_data: Project,
    ):
        member = ProjectMember(
            id="user-1", name="Owner", email="owner@test.com", role=RoleEnum.OWNER
        )
        when(mock_project_repository).get_by_id(project_data.id).thenReturn(project_data)
        when(mock_project_repository).get_project_members(project_data.id).thenReturn([member])
        when(mock_project_repository).update(project_data).thenReturn(None)

        with pytest.raises(CannotUpdateException, match=Constants.PROJECT_NOT_UPDATED):
            update_project_use_case.execute("user-1", project_data)

        verify(mock_project_repository).update(project_data)
