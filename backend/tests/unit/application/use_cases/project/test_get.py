from mockito import verify, when, ANY

import pytest

from application.use_cases.project.get import GetProjectUseCase
from domain.entities.project import Project, ProjectBoard, ProjectFilters
from domain.exceptions.not_found_exception import NotFoundException
from domain.repositories.project_repository import ProjectRepository
from domain.utils.constants import Constants


class TestGetProjectUseCase:
    @pytest.fixture
    def project(self) -> Project:
        return Project(
            title="Project",
            description="A description",
            client="Client",
            delivery_date="2026-12-31",
        )

    def test_execute_paginated_summary(
        self,
        get_project_use_case: GetProjectUseCase,
        mock_project_repository: ProjectRepository,
    ):
        expected = (1, ["summary"])
        when(mock_project_repository).get_paginated_dashboard_projects(
            user_id="user-1", page=1, page_size=10, filters=None
        ).thenReturn(expected)

        result = get_project_use_case.execute_paginated_summary("user-1", 1, 10)

        assert result == expected
        verify(mock_project_repository).get_paginated_dashboard_projects(
            user_id="user-1", page=1, page_size=10, filters=None
        )

    def test_execute_paginated_summary_with_filters(
        self,
        get_project_use_case: GetProjectUseCase,
        mock_project_repository: ProjectRepository,
    ):
        filters = ProjectFilters(search="abc")
        when(mock_project_repository).get_paginated_dashboard_projects(
            user_id="user-1", page=2, page_size=5, filters=filters
        ).thenReturn((0, []))

        result = get_project_use_case.execute_paginated_summary("user-1", 2, 5, filters)

        assert result == (0, [])
        verify(mock_project_repository).get_paginated_dashboard_projects(
            user_id="user-1", page=2, page_size=5, filters=filters
        )

    def test_execute_returns_project(
        self,
        get_project_use_case: GetProjectUseCase,
        mock_project_repository: ProjectRepository,
        project: Project,
    ):
        when(mock_project_repository).get_by_id("project-1").thenReturn(project)

        result = get_project_use_case.execute("project-1")

        assert result == project
        verify(mock_project_repository).get_by_id("project-1")

    def test_execute_raises_when_not_found(
        self,
        get_project_use_case: GetProjectUseCase,
        mock_project_repository: ProjectRepository,
    ):
        when(mock_project_repository).get_by_id("project-1").thenReturn(None)

        with pytest.raises(NotFoundException, match=Constants.PROJECT_NOT_FOUND):
            get_project_use_case.execute("project-1")

        verify(mock_project_repository).get_by_id("project-1")

    def test_get_project_members_succesfully(
        self,
        get_project_use_case: GetProjectUseCase,
        mock_project_repository: ProjectRepository,
        project: Project,
    ):
        members = ["member-1", "member-2"]
        when(mock_project_repository).get_by_id("project-1").thenReturn(project)
        when(mock_project_repository).get_project_members("project-1").thenReturn(members)

        result = get_project_use_case.execute_get_project_members("project-1")

        assert result == members
        verify(mock_project_repository).get_by_id("project-1")
        verify(mock_project_repository).get_project_members("project-1")

    def test_get_project_members_raises_when_not_found(
        self,
        get_project_use_case: GetProjectUseCase,
        mock_project_repository: ProjectRepository,
    ):
        when(mock_project_repository).get_by_id("project-1").thenReturn(None)

        with pytest.raises(NotFoundException, match=Constants.PROJECT_NOT_FOUND):
            get_project_use_case.execute_get_project_members("project-1")

        verify(mock_project_repository).get_by_id("project-1")
        verify(mock_project_repository, times=0).get_project_members(ANY(str))

    def test_get_project_board_succesfully(
        self,
        get_project_use_case: GetProjectUseCase,
        mock_project_repository: ProjectRepository,
        project: Project,
    ):
        board = ProjectBoard(project_id=str(project.id), project_title="Project", columns=[])
        when(mock_project_repository).get_by_id("project-1").thenReturn(project)
        when(mock_project_repository).get_project_board("project-1", filters=None).thenReturn(board)

        result = get_project_use_case.execute_get_project_board("project-1")

        assert result == board
        verify(mock_project_repository).get_by_id("project-1")
        verify(mock_project_repository).get_project_board("project-1", filters=None)

    def test_get_project_board_raises_when_not_found(
        self,
        get_project_use_case: GetProjectUseCase,
        mock_project_repository: ProjectRepository,
    ):
        when(mock_project_repository).get_by_id("project-1").thenReturn(None)

        with pytest.raises(NotFoundException, match=Constants.PROJECT_NOT_FOUND):
            get_project_use_case.execute_get_project_board("project-1")

        verify(mock_project_repository).get_by_id("project-1")
        verify(mock_project_repository, times=0).get_project_board(ANY(str), filters=ANY)
