from datetime import datetime, timedelta
import secrets

from application.interfaces.email_sender import EmailSender
from domain.entities.enums import InvitationStatusEnum
from domain.entities.user import User
from domain.exceptions.not_found_exception import NotFoundException
from domain.exceptions.resource_alredy_exists_exception import ResourceAlreadyExistsException
from domain.repositories.invitation_repository import InvitationRepository
from domain.repositories.project_repository import ProjectRepository
from domain.repositories.user_project_link_repository import UserProjectLinkRepository
from domain.repositories.user_repository import UserRepository
from domain.entities.project_invitation import ProjectInvitation
from domain.utils.constants import Constants
from domain.exceptions.forbidden_exception import ForbiddenException


class InviteMemberUseCase:
    def __init__(
        self,
        repository: InvitationRepository,
        project_repository: ProjectRepository,
        user_repository: UserRepository,
        user_project_link_repository: UserProjectLinkRepository,
        email_sender: EmailSender,
    ):
        self.repository = repository
        self.project_repository = project_repository
        self.user_repository = user_repository
        self.user_project_link_repository = user_project_link_repository
        self.email_sender = email_sender

    def execute(self, current_user: User, project_id: str, invitee_email: str) -> None:
        project = self.project_repository.get_by_id(project_id)
        if not project:
            raise NotFoundException(Constants.PROJECT_NOT_FOUND)

        if not self.user_project_link_repository.get_by_user_and_project(
            current_user.id, project_id
        ):
            raise ForbiddenException(Constants.PROJECT_FORBIDDEN)

        invitee = self.user_repository.get_by_email(invitee_email)

        if not invitee:
            raise NotFoundException(Constants.INVITEE_NOT_REGISTERED)

        if self.user_project_link_repository.get_by_user_and_project(invitee.id, project_id):
            raise ResourceAlreadyExistsException(Constants.ALREADY_MEMBER)

        if self.repository.has_alredy_been_sent_invitation(invitee_email, project_id):
            raise ResourceAlreadyExistsException(Constants.INVITATION_ALREADY_SENT)

        token = secrets.token_urlsafe(32)
        expires_at = datetime.now() + timedelta(days=7)

        invitation = ProjectInvitation(
            invitee_email=invitee_email,
            status=InvitationStatusEnum.PENDING,
            token=token,
            project_id=project_id,
            invited_by=current_user.id,
            expires_at=expires_at,
            created_at=datetime.now(),
        )

        invitation.token = token
        invitation.expires_at = expires_at

        self.repository.create(invitation)

        self.email_sender.send_project_invitation_email(
            to_email=invitation.invitee_email,
            sender_name=current_user.name,
            project_title=project.title,
            verification_token=token,
        )
