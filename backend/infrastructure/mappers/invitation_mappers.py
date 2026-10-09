from domain.entities.project_invitation import ProjectInvitation
from infrastructure.db.models.project_invitation_model import ProjectInvitationModel


def map_invitation_entity_to_model(project_invitation: ProjectInvitation) -> ProjectInvitationModel:
    return ProjectInvitationModel(
        id=project_invitation.id,
        token=project_invitation.token,
        invitee_email=project_invitation.invitee_email,
        status=project_invitation.status,
        project_id=project_invitation.project_id,
        invited_by=project_invitation.invited_by,
        expires_at=project_invitation.expires_at,
        created_at=project_invitation.created_at,
    )


def map_invitation_model_to_entity(project_invitation: ProjectInvitationModel) -> ProjectInvitation:
    return ProjectInvitation(
        id=project_invitation.id,
        token=project_invitation.token,
        invitee_email=project_invitation.invitee_email,
        status=project_invitation.status,
        project_id=project_invitation.project_id,
        invited_by=project_invitation.invited_by,
        expires_at=project_invitation.expires_at,
        created_at=project_invitation.created_at,
    )
