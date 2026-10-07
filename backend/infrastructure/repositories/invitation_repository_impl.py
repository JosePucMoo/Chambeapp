from sqlalchemy import select
from sqlalchemy.orm import Session

from infrastructure.db.models.user_model import UserModel
from infrastructure.db.models.project_model import ProjectModel
from domain.entities.enums import InvitationStatusEnum
from infrastructure.mappers.invitation_mappers import (
    map_invitation_entity_to_model,
    map_invitation_model_to_entity,
)
from infrastructure.db.models.project_invitation_model import ProjectInvitationModel
from domain.entities.project_invitation import InvitationPreview, ProjectInvitation
from domain.repositories.invitation_repository import InvitationRepository


class InvitationRepositoryImpl(InvitationRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_token(self, token: str) -> InvitationPreview:
        query = (
            select(
                ProjectInvitationModel.invitee_email,
                ProjectInvitationModel.status,
                ProjectInvitationModel.expires_at,
                ProjectModel.title,
                UserModel.name,
            )
            .where(ProjectInvitationModel.token == token)
            .join(ProjectModel, ProjectModel.id == ProjectInvitationModel.project_id)
        )

        result = self.db.execute(query).first()

        if not result:
            return None

        return InvitationPreview(
            owner_name=result.name,
            project_title=result.title,
            invitee_email=result.invitee_email,
            status=result.status,
            expires_at=result.expires_at,
        )

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
