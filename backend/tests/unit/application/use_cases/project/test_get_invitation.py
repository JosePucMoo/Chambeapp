from datetime import datetime, timedelta

from mockito import verify, when

import pytest

from application.use_cases.project.get_invitation import GetInvitationUseCase
from domain.entities.enums import InvitationStatusEnum
from domain.entities.project_invitation import InvitationPreview
from domain.exceptions.not_found_exception import NotFoundException
from domain.exceptions.resource_expired_exception import ResourceExpiredException
from domain.repositories.invitation_repository import InvitationRepository
from domain.utils.constants import Constants


class TestGetInvitationUseCase:
    @pytest.fixture
    def token(self) -> str:
        return "invitation_token"

    @pytest.fixture
    def preview(self) -> InvitationPreview:
        return InvitationPreview(
            owner_name="Owner",
            project_title="Project",
            invitee_email="invitee@test.com",
            status=InvitationStatusEnum.PENDING,
            expires_at=datetime.now() + timedelta(days=1),
        )

    def test_get_invitation_succesfully(
        self,
        get_invitation_use_case: GetInvitationUseCase,
        mock_invitation_repository: InvitationRepository,
        token: str,
        preview: InvitationPreview,
    ):
        when(mock_invitation_repository).get_token_preview(token=token).thenReturn(preview)

        result = get_invitation_use_case.execute(token)

        assert result == preview
        verify(mock_invitation_repository).get_token_preview(token=token)

    def test_invitation_not_found(
        self,
        get_invitation_use_case: GetInvitationUseCase,
        mock_invitation_repository: InvitationRepository,
        token: str,
    ):
        when(mock_invitation_repository).get_token_preview(token=token).thenReturn(None)

        with pytest.raises(NotFoundException, match=Constants.INVITATION_NOT_FOUND):
            get_invitation_use_case.execute(token)

        verify(mock_invitation_repository).get_token_preview(token=token)

    def test_invitation_expired(
        self,
        get_invitation_use_case: GetInvitationUseCase,
        mock_invitation_repository: InvitationRepository,
        token: str,
        preview: InvitationPreview,
    ):
        preview.expires_at = datetime.now() - timedelta(days=1)
        when(mock_invitation_repository).get_token_preview(token=token).thenReturn(preview)

        with pytest.raises(ResourceExpiredException, match=Constants.INVITATION_EXPIRED):
            get_invitation_use_case.execute(token)

        verify(mock_invitation_repository).get_token_preview(token=token)
