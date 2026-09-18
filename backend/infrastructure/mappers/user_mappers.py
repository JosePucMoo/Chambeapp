from infrastructure.db.models.user_model import UserModel
from domain.entities.user import User
from infrastructure.schemas.user_schema import CreateUserDTO


def map_create_user_dto_to_entity(user_dto: CreateUserDTO):
    return User(
        name=user_dto.name,
        email=user_dto.email,
        hashed_password=user_dto.password
    )

def map_user_entity_to_model(user: User) -> UserModel:
    return UserModel(
        id= user.id,
        name=user.name,
        email=user.email,
        password=user.password,
        token=user.token,
        is_verified=user.is_verified
    )

def map_user_model_to_entity(user_model: UserModel) -> User:
    return User(
        id=user_model.id,
        name=user_model.name,
        email=user_model.email,
        token=user_model.token,
        hashed_password=user_model.password,
        is_verified=user_model.is_verified
    )