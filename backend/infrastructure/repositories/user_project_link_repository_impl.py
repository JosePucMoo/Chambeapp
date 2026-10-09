from sqlalchemy import select
from sqlalchemy.orm import Session

from infrastructure.db.models.user_project_link_model import UserProjectLinkModel
from infrastructure.mappers.user_project_link_mappers import (
    map_user_project_link_entity_to_model,
    map_user_project_link_model_to_entity,
)
from domain.entities.user_project_link import UserProjectLink
from domain.repositories.user_project_link_repository import UserProjectLinkRepository


class UserProjectLinkRepositoryImpl(UserProjectLinkRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_project_link: UserProjectLink) -> UserProjectLink:
        user_project_link_model = map_user_project_link_entity_to_model(user_project_link)

        self.db.add(user_project_link_model)
        self.db.commit()
        self.db.refresh(user_project_link_model)

        return map_user_project_link_model_to_entity(user_project_link_model)

    def get_by_user_and_project(self, user_id: str, project_id: str) -> UserProjectLink:
        query = select(UserProjectLinkModel).where(
            UserProjectLinkModel.user_id == user_id, UserProjectLinkModel.project_id == project_id
        )

        model = self.db.scalar(query)

        return map_user_project_link_model_to_entity(model) if model else None
