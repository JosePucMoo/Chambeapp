from mockito import verify, when, ANY

import pytest

from application.interfaces.email_sender import EmailSender
from application.use_cases.project.invite_member import InviteMemberUseCase
from domain.entities.enums import InvitationStatusEnum
from domain.entities.project import Project
from domain.entities.project_invitation import ProjectInvitation
from domain.entities.user import User
from domain.entities.user_project_link import UserProjectLink
from domain.exceptions.forbidden_exception import ForbiddenException
from domain.exceptions.not_found_exception import NotFoundException
from domain.exceptions.resource_alredy_exists_exception import ResourceAlreadyExistsException
from domain.repositories.invitation_repository import InvitationRepository
from domain.repositories.project_repository import ProjectRepository
from domain.repositories.user_project_link_repository import UserProjectLinkRepository
from domain.repositories.user_repository import UserRepository
from domain.utils.constants import Constants


class TestInviteMemberUseCase:
    @pytest.fixture
    def current_user(self) -> User:
        return User(
            id="owner-1",
            name="Owner",
            email="owner@test.com",
            password="hashed",
            is_verified=True,
        )

    @pytest.fixture
    def project(self) -> Project:
        return Project(
            title="Project",
            description="A description",
            client="Client",
            delivery_date="2026-12-31",
        )

    @pytest.fixture
    def invitee(self) -> User:
        return User(
            id="invitee-1",
            name="Invitee",
            email="invitee@test.com",
            password="hashed",
            is_verified=True,
        )

    def test_invite_succesfully(
        self,
        invite_member_use_case: InviteMemberUseCase,
        mock_invitation_repository: InvitationRepository,
        mock_project_repository: ProjectRepository,
        mock_user_repository: UserRepository,
        mock_user_project_link_repository: UserProjectLinkRepository,
        mock_email_sender: EmailSender,
        current_user: User,
        project: Project,
        invitee: User,
    ):
        when(mock_project_repository).get_by_id(project.id).thenReturn(project)
        when(mock_user_project_link_repository).get_by_user_and_project(
            current_user.id, project.id
        ).thenReturn(UserProjectLink(role="Owner", user_id=current_user.id, project_id=project.id))
        when(mock_user_repository).get_by_email(invitee.email).thenReturn(invitee)
        when(mock_user_project_link_repository).get_by_user_and_project(
            invitee.id, project.id
        ).thenReturn(None)
        when(mock_invitation_repository).has_alredy_been_sent_invitation(
            invitee.email, project.id
        ).thenReturn(False)

        captured = {}
        when(mock_invitation_repository).create(ANY(ProjectInvitation)).thenAnswer(
            lambda invitation: captured.setdefault("invitation", invitation)
        )

        when(mock_email_sender).send_project_invitation_email(
            to_email=invitee.email,
            sender_name=current_user.name,
            project_title=project.title,
            verification_token=ANY(str),
        ).thenReturn(None)

        result = invite_member_use_case.execute(current_user, project.id, invitee.email)

        assert result is None

        invitation = captured["invitation"]
        assert isinstance(invitation, ProjectInvitation)
        assert invitation.invitee_email == invitee.email
        assert invitation.status == InvitationStatusEnum.PENDING
        assert invitation.project_id == project.id
        assert invitation.invited_by == current_user.id
        assert invitation.token is not None
        assert invitation.expires_at is not None

        verify(mock_project_repository).get_by_id(project.id)
        verify(mock_user_repository).get_by_email(invitee.email)
        verify(mock_invitation_repository).create(ANY(ProjectInvitation))
        verify(mock_email_sender).send_project_invitation_email(
            to_email=invitee.email,
            sender_name=current_user.name,
            project_title=project.title,
            verification_token=ANY(str),
        )

    def test_project_not_found(
        self,
        invite_member_use_case: InviteMemberUseCase,
        mock_project_repository: ProjectRepository,
        mock_user_project_link_repository: UserProjectLinkRepository,
        current_user: User,
        project: Project,
        invitee: User,
    ):
        when(mock_project_repository).get_by_id(project.id).thenReturn(None)

        with pytest.raises(NotFoundException, match=Constants.PROJECT_NOT_FOUND):
            invite_member_use_case.execute(current_user, project.id, invitee.email)

        verify(mock_project_repository).get_by_id(project.id)
        verify(mock_user_project_link_repository, times=0).get_by_user_and_project(ANY, ANY)

    def test_current_user_not_member(
        self,
        invite_member_use_case: InviteMemberUseCase,
        mock_project_repository: ProjectRepository,
        mock_user_project_link_repository: UserProjectLinkRepository,
        current_user: User,
        project: Project,
        invitee: User,
    ):
        when(mock_project_repository).get_by_id(project.id).thenReturn(project)
        when(mock_user_project_link_repository).get_by_user_and_project(
            current_user.id, project.id
        ).thenReturn(None)

        with pytest.raises(ForbiddenException, match=Constants.PROJECT_FORBIDDEN):
            invite_member_use_case.execute(current_user, project.id, invitee.email)

        verify(mock_user_project_link_repository).get_by_user_and_project(current_user.id, project.id)

    def test_invitee_not_registered(
        self,
        invite_member_use_case: InviteMemberUseCase,
        mock_project_repository: ProjectRepository,
        mock_user_repository: UserRepository,
        mock_user_project_link_repository: UserProjectLinkRepository,
        current_user: User,
        project: Project,
        invitee: User,
    ):
        link = UserProjectLink(
            role="owner", user_id=current_user.id, project_id=project.id
        )
        when(mock_project_repository).get_by_id(project.id).thenReturn(project)
        when(mock_user_project_link_repository).get_by_user_and_project(
            current_user.id, project.id
        ).thenReturn(link)
        when(mock_user_repository).get_by_email(invitee.email).thenReturn(None)

        with pytest.raises(NotFoundException, match=Constants.INVITEE_NOT_REGISTERED):
            invite_member_use_case.execute(current_user, project.id, invitee.email)

        verify(mock_user_repository).get_by_email(invitee.email)

    def test_invitee_already_member(
        self,
        invite_member_use_case: InviteMemberUseCase,
        mock_project_repository: ProjectRepository,
        mock_user_repository: UserRepository,
        mock_user_project_link_repository: UserProjectLinkRepository,
        current_user: User,
        project: Project,
        invitee: User,
    ):
        link = UserProjectLink(role="owner", user_id=current_user.id, project_id=project.id)
        invitee_link = UserProjectLink(
            role="guest", user_id=invitee.id, project_id=project.id
        )
        when(mock_project_repository).get_by_id(project.id).thenReturn(project)
        when(mock_user_project_link_repository).get_by_user_and_project(
            current_user.id, project.id
        ).thenReturn(link)
        when(mock_user_repository).get_by_email(invitee.email).thenReturn(invitee)
        when(mock_user_project_link_repository).get_by_user_and_project(
            invitee.id, project.id
        ).thenReturn(invitee_link)

        with pytest.raises(ResourceAlreadyExistsException, match=Constants.ALREADY_MEMBER):
            invite_member_use_case.execute(current_user, project.id, invitee.email)

        verify(mock_user_project_link_repository).get_by_user_and_project(invitee.id, project.id)

    def test_invitation_already_sent(
        self,
        invite_member_use_case: InviteMemberUseCase,
        mock_invitation_repository: InvitationRepository,
        mock_project_repository: ProjectRepository,
        mock_user_repository: UserRepository,
        mock_user_project_link_repository: UserProjectLinkRepository,
        current_user: User,
        project: Project,
        invitee: User,
    ):
        link = UserProjectLink(role="owner", user_id=current_user.id, project_id=project.id)
        when(mock_project_repository).get_by_id(project.id).thenReturn(project)
        when(mock_user_project_link_repository).get_by_user_and_project(
            current_user.id, project.id
        ).thenReturn(link)
        when(mock_user_repository).get_by_email(invitee.email).thenReturn(invitee)
        when(mock_user_project_link_repository).get_by_user_and_project(
            invitee.id, project.id
        ).thenReturn(None)
        when(mock_invitation_repository).has_alredy_been_sent_invitation(
            invitee.email, project.id
        ).thenReturn(True)

        with pytest.raises(
            ResourceAlreadyExistsException, match=Constants.INVITATION_ALREADY_SENT
        ):
            invite_member_use_case.execute(current_user, project.id, invitee.email)

        verify(mock_invitation_repository).has_alredy_been_sent_invitation(
            invitee.email, project.id
        )
        verify(mock_invitation_repository, times=0).create(ANY(ProjectInvitation))
