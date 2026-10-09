from domain.entities.user_project_link import UserProjectLink
from infrastructure.db.models.user_project_link_model import UserProjectLinkModel


def map_user_project_link_entity_to_model(
    user_project_link: UserProjectLink,
) -> UserProjectLinkModel:
    return UserProjectLinkModel(
        id=user_project_link.id,
        role=user_project_link.role,
        user_id=user_project_link.user_id,
        project_id=user_project_link.project_id,
    )


def map_user_project_link_model_to_entity(
    user_project_link: UserProjectLinkModel,
) -> UserProjectLink:
    return UserProjectLink(
        id=user_project_link.id,
        role=user_project_link.role,
        user_id=user_project_link.user_id,
        project_id=user_project_link.project_id,
    )
