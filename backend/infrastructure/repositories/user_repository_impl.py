
from sqlalchemy import select
from sqlalchemy.orm import Session
from infrastructure.db.models.user_model import UserModel
from infrastructure.mappers.user_mappers import map_user_entity_to_model, map_user_model_to_entity
from domain.repositories.user_repository import UserRepository
from domain.entities.user import User 


class UserRepositoryImpl(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, user: User) -> User:
        user_model = map_user_entity_to_model(user)
        self.db.add(user_model)
        self.db.commit()
        self.db.refresh(user_model)

        return map_user_model_to_entity(user_model)

    def get_by_email(self, email:str) -> User | None:
        query = select(UserModel).where(UserModel.email == email)
        return self.db.scalars(query).one_or_none()