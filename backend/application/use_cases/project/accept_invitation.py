from datetime import datetime

from domain.entities.enums import InvitationStatusEnum, RoleEnum
from domain.entities.user import User
from domain.entities.user_project_link import UserProjectLink
from domain.exceptions.forbidden_exception import ForbiddenException
from domain.exceptions.not_found_exception import NotFoundException
from domain.exceptions.resource_expired_exception import ResourceExpiredException
from domain.repositories.invitation_repository import InvitationRepository
from domain.repositories.user_project_link_repository import UserProjectLinkRepository
from domain.utils.constants import Constants


class AcceptInvitationUseCase:
    def __init__(
        self,
        repository: InvitationRepository,
        user_project_link_repository: UserProjectLinkRepository,
    ):
        self.repository = repository
        self.user_project_link_repository = user_project_link_repository

    def execute(self, token: str, current_user: User) -> str:
        invitation = self.repository.get_by_token(token=token)

        if not invitation:
            raise NotFoundException(Constants.INVITATION_NOT_FOUND)

        if invitation.expires_at < datetime.now():
            raise ResourceExpiredException(Constants.INVITATION_EXPIRED)

        if invitation.invitee_email != current_user.email:
            raise ForbiddenException(Constants.INVITATION_FORBIDDEN)

        project_id = invitation.project_id

        if self.user_project_link_repository.get_by_user_and_project(
            user_id=current_user.id, project_id=project_id
        ):
            return project_id

        user_project_link = UserProjectLink(
            role=RoleEnum.GUEST, user_id=current_user.id, project_id=project_id
        )
        self.user_project_link_repository.create(user_project_link)
        self.repository.update_status(token=token, status=InvitationStatusEnum.ACCEPTED)

        return project_id
