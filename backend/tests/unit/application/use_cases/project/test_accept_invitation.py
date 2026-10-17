from datetime import datetime, timedelta

from mockito import verify, when, ANY

import pytest

from application.use_cases.project.accept_invitation import AcceptInvitationUseCase
from domain.entities.enums import InvitationStatusEnum, RoleEnum
from domain.entities.project_invitation import ProjectInvitation
from domain.entities.user import User
from domain.entities.user_project_link import UserProjectLink
from domain.exceptions.forbidden_exception import ForbiddenException
from domain.exceptions.not_found_exception import NotFoundException
from domain.exceptions.resource_expired_exception import ResourceExpiredException
from domain.repositories.invitation_repository import InvitationRepository
from domain.repositories.user_project_link_repository import UserProjectLinkRepository
from domain.utils.constants import Constants


class TestAcceptInvitationUseCase:
    @pytest.fixture
    def token(self) -> str:
        return "invitation_token"

    @pytest.fixture
    def current_user(self) -> User:
        return User(
            id="user-1",
            name="Invitee",
            email="invitee@test.com",
            password="hashed",
            is_verified=True,
        )

    @pytest.fixture
    def invitation(self) -> ProjectInvitation:
        return ProjectInvitation(
            invitee_email="invitee@test.com",
            status=InvitationStatusEnum.PENDING,
            project_id="project-1",
            invited_by="owner-1",
            token="invitation_token",
            expires_at=datetime.now() + timedelta(days=1),
        )

    def test_accept_succesfully(
        self,
        accept_invitation_use_case: AcceptInvitationUseCase,
        mock_invitation_repository: InvitationRepository,
        mock_user_project_link_repository: UserProjectLinkRepository,
        token: str,
        current_user: User,
        invitation: ProjectInvitation,
    ):
        when(mock_invitation_repository).get_by_token(token=token).thenReturn(invitation)
        when(mock_user_project_link_repository).get_by_user_and_project(
            user_id=current_user.id, project_id=invitation.project_id
        ).thenReturn(None)

        captured_link = {}
        when(mock_user_project_link_repository).create(ANY(UserProjectLink)).thenAnswer(
            lambda link: captured_link.setdefault("value", link)
        )

        when(mock_invitation_repository).update_status(
            token=token, status=InvitationStatusEnum.ACCEPTED
        ).thenReturn(invitation)

        result = accept_invitation_use_case.execute(token, current_user)

        assert result == invitation.project_id

        link = captured_link["value"]
        assert isinstance(link, UserProjectLink)
        assert link.role == RoleEnum.GUEST
        assert link.user_id == current_user.id
        assert link.project_id == invitation.project_id

        verify(mock_invitation_repository).get_by_token(token=token)
        verify(mock_user_project_link_repository).create(ANY(UserProjectLink))
        verify(mock_invitation_repository).update_status(
            token=token, status=InvitationStatusEnum.ACCEPTED
        )

    def test_invitation_not_found(
        self,
        accept_invitation_use_case: AcceptInvitationUseCase,
        mock_invitation_repository: InvitationRepository,
        mock_user_project_link_repository: UserProjectLinkRepository,
        token: str,
        current_user: User,
    ):
        when(mock_invitation_repository).get_by_token(token=token).thenReturn(None)

        with pytest.raises(NotFoundException, match=Constants.INVITATION_NOT_FOUND):
            accept_invitation_use_case.execute(token, current_user)

        verify(mock_invitation_repository).get_by_token(token=token)
        verify(mock_user_project_link_repository, times=0).get_by_user_and_project(ANY, ANY)

    def test_invitation_expired(
        self,
        accept_invitation_use_case: AcceptInvitationUseCase,
        mock_invitation_repository: InvitationRepository,
        token: str,
        current_user: User,
        invitation: ProjectInvitation,
    ):
        invitation.expires_at = datetime.now() - timedelta(days=1)
        when(mock_invitation_repository).get_by_token(token=token).thenReturn(invitation)

        with pytest.raises(ResourceExpiredException, match=Constants.INVITATION_EXPIRED):
            accept_invitation_use_case.execute(token, current_user)

        verify(mock_invitation_repository).get_by_token(token=token)

    def test_email_mismatch(
        self,
        accept_invitation_use_case: AcceptInvitationUseCase,
        mock_invitation_repository: InvitationRepository,
        mock_user_project_link_repository: UserProjectLinkRepository,
        token: str,
        current_user: User,
        invitation: ProjectInvitation,
    ):
        invitation.invitee_email = "other@test.com"
        when(mock_invitation_repository).get_by_token(token=token).thenReturn(invitation)

        with pytest.raises(ForbiddenException, match=Constants.INVITATION_FORBIDDEN):
            accept_invitation_use_case.execute(token, current_user)

        verify(mock_user_project_link_repository, times=0).get_by_user_and_project(ANY, ANY)

    def test_user_already_member(
        self,
        accept_invitation_use_case: AcceptInvitationUseCase,
        mock_invitation_repository: InvitationRepository,
        mock_user_project_link_repository: UserProjectLinkRepository,
        token: str,
        current_user: User,
        invitation: ProjectInvitation,
    ):
        existing_link = UserProjectLink(
            role=RoleEnum.GUEST, user_id=current_user.id, project_id=invitation.project_id
        )
        when(mock_invitation_repository).get_by_token(token=token).thenReturn(invitation)
        when(mock_user_project_link_repository).get_by_user_and_project(
            user_id=current_user.id, project_id=invitation.project_id
        ).thenReturn(existing_link)

        result = accept_invitation_use_case.execute(token, current_user)

        assert result == invitation.project_id
        verify(mock_user_project_link_repository, times=0).create(ANY(UserProjectLink))
        verify(mock_invitation_repository, times=0).update_status(token=ANY, status=ANY)
