from typing import List

from sqlalchemy import select, func
from sqlalchemy.orm import Session
from infrastructure.mappers.user_mappers import map_user_entity_to_model, map_user_model_to_entity
from infrastructure.db.models.user_model import UserModel
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

    def get_by_email(self, email: str) -> User | None:
        query = select(UserModel).where(UserModel.email == email)
        user = self.db.scalars(query).one_or_none()

        return map_user_model_to_entity(user) if user else None

    def get_all(self, page: int, page_size: int) -> List[User]:
        count_query = select(func.count()).select_from(UserModel)
        total_count = self.db.execute(count_query).scalar()

        offset = (page - 1) * page_size
        query = select(UserModel).offset(offset).limit(page_size)

        user_models = self.db.scalars(query).all()

        users = [map_user_model_to_entity(user_model) for user_model in user_models]

        return users, total_count

    def get_by_id(self, id: str) -> User | None:
        query = select(UserModel).where(UserModel.id == id)
        user = self.db.scalar(query)

        if not user:
            return None

        return map_user_model_to_entity(user)

    def update(self, user: User) -> User:
        query = select(UserModel).where(UserModel.id == user.id)
        user_updated = self.db.scalar(query)

        user_updated.name = user.name
        user_updated.email = user.email
        user_updated.password = user.password
        user_updated.is_verified = user.is_verified
        user_updated.token = user.token

        self.db.commit()
        self.db.refresh(user_updated)

        return map_user_model_to_entity(user_updated)

    def get_by_token(self, token: str) -> User | None:
        query = select(UserModel).where(UserModel.token == token)
        user = self.db.scalar(query)
        return map_user_model_to_entity(user) if user else None
