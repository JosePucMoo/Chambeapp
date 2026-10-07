from datetime import datetime

from domain.entities.project_invitation import InvitationPreview
from domain.utils.constants import Constants
from domain.exceptions.not_found_exception import NotFoundException
from domain.exceptions.resource_expired_exception import ResourceExpiredException
from domain.repositories.invitation_repository import InvitationRepository


class GetInvitationUseCase:
    def __init__(self, repository: InvitationRepository):
        self.repository = repository

    def execute(self, token: str) -> InvitationPreview:
        invitation = self.repository.get_by_token(token=token)

        if not invitation:
            raise NotFoundException(Constants.INVITATION_NOT_FOUND)

        if invitation.expires_at < datetime.now():
            raise ResourceExpiredException(Constants.INVITATION_EXPIRED)

        return invitation
