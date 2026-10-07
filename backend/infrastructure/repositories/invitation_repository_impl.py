from sqlalchemy import select
from sqlalchemy.orm import Session

from domain.entities.enums import InvitationStatusEnum
from infrastructure.mappers.invitation_mappers import (
    map_invitation_entity_to_model,
    map_invitation_model_to_entity,
)
from infrastructure.db.models.project_invitation_model import ProjectInvitationModel
from domain.entities.project_invitation import ProjectInvitation
from domain.repositories.invitation_repository import InvitationRepository


class InvitationRepositoryImpl(InvitationRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_token(self, token: str) -> ProjectInvitation:
        query = select(ProjectInvitationModel).where(ProjectInvitationModel.token == token)

        invitation_model = self.db.scalar(query)

        return map_invitation_model_to_entity(invitation_model) if invitation_model else None

    def create(self, project_invitation: ProjectInvitation) -> ProjectInvitation:
        invitation_model = map_invitation_entity_to_model(project_invitation)

        self.db.add(invitation_model)
        self.db.commit()
        self.db.refresh(invitation_model)

        return map_invitation_model_to_entity(invitation_model)

    def has_alredy_been_sent_invitation(self, invitee_email: str, project_id: str) -> bool:
        query = select(ProjectInvitationModel).where(
            ProjectInvitationModel.invitee_email == invitee_email
            and ProjectInvitationModel.project_id == project_id
        )

        invitation_model = self.db.scalar(query)

        if not invitation_model:
            return False

        return invitation_model.status == InvitationStatusEnum.PENDING
