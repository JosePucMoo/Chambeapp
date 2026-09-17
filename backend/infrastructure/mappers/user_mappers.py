from infrastructure.db.models.user_model import UserModel
from domain.entities.user import UpdateProfileUser, User
from infrastructure.schemas.user_schema import CreateUserDTO, UpdateProfileUserDTO


def map_create_user_dto_to_entity(user_dto: CreateUserDTO):
    return User(
        name=user_dto.name,
        email=user_dto.email,
        password=user_dto.password
    )

def map_user_entity_to_model(user: User) -> UserModel:
    return UserModel(
        id= user.id,
        name=user.name,
        email=user.email,
        password=user.password,
        is_verified=user.is_verified
    )

def map_user_model_to_entity(user_model: UserModel) -> User:
    return User(
        id=user_model.id,
        name=user_model.name,
        email=user_model.email,
        password=user_model.password,
        is_verified=user_model.is_verified
    )

def map_update_profile_user_dto_to_entity(id: str, user_dto: UpdateProfileUserDTO):
    return UpdateProfileUser(
        id=id,
        name=user_dto.name
    )