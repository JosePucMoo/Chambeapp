from mockito import mock
import pytest

from application.interfaces.email_sender import EmailSender
from application.use_cases.project.accept_invitation import AcceptInvitationUseCase
from application.use_cases.project.create import CreateProjectUseCase
from application.use_cases.project.get import GetProjectUseCase
from application.use_cases.project.get_invitation import GetInvitationUseCase
from application.use_cases.project.invite_member import InviteMemberUseCase
from application.use_cases.project.update import UpdateProjectUseCase
from domain.repositories.column_repository import ColumnRepository
from domain.repositories.invitation_repository import InvitationRepository
from domain.repositories.project_repository import ProjectRepository
from domain.repositories.user_project_link_repository import UserProjectLinkRepository
from domain.repositories.user_repository import UserRepository


@pytest.fixture
def mock_project_repository() -> ProjectRepository:
    return mock(ProjectRepository)


@pytest.fixture
def mock_column_repository() -> ColumnRepository:
    return mock(ColumnRepository)


@pytest.fixture
def mock_user_project_link_repository() -> UserProjectLinkRepository:
    return mock(UserProjectLinkRepository)


@pytest.fixture
def mock_invitation_repository() -> InvitationRepository:
    return mock(InvitationRepository)


@pytest.fixture
def mock_user_repository() -> UserRepository:
    return mock(UserRepository)


@pytest.fixture
def mock_email_sender() -> EmailSender:
    return mock(EmailSender)


@pytest.fixture
def create_project_use_case(
    mock_project_repository: ProjectRepository,
    mock_column_repository: ColumnRepository,
    mock_user_project_link_repository: UserProjectLinkRepository,
) -> CreateProjectUseCase:
    return CreateProjectUseCase(
        repository=mock_project_repository,
        column_repository=mock_column_repository,
        user_project_link_repository=mock_user_project_link_repository,
    )


@pytest.fixture
def get_project_use_case(mock_project_repository: ProjectRepository) -> GetProjectUseCase:
    return GetProjectUseCase(repository=mock_project_repository)


@pytest.fixture
def update_project_use_case(mock_project_repository: ProjectRepository) -> UpdateProjectUseCase:
    return UpdateProjectUseCase(repository=mock_project_repository)


@pytest.fixture
def invite_member_use_case(
    mock_invitation_repository: InvitationRepository,
    mock_project_repository: ProjectRepository,
    mock_user_repository: UserRepository,
    mock_user_project_link_repository: UserProjectLinkRepository,
    mock_email_sender: EmailSender,
) -> InviteMemberUseCase:
    return InviteMemberUseCase(
        repository=mock_invitation_repository,
        project_repository=mock_project_repository,
        user_repository=mock_user_repository,
        user_project_link_repository=mock_user_project_link_repository,
        email_sender=mock_email_sender,
    )


@pytest.fixture
def accept_invitation_use_case(
    mock_invitation_repository: InvitationRepository,
    mock_user_project_link_repository: UserProjectLinkRepository,
) -> AcceptInvitationUseCase:
    return AcceptInvitationUseCase(
        repository=mock_invitation_repository,
        user_project_link_repository=mock_user_project_link_repository,
    )


@pytest.fixture
def get_invitation_use_case(
    mock_invitation_repository: InvitationRepository,
) -> GetInvitationUseCase:
    return GetInvitationUseCase(repository=mock_invitation_repository)
