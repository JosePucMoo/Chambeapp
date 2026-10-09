from infrastructure.schemas.auth_schema import RegisterDTO, UserResponseDTO
from infrastructure.db.models.user_model import UserModel
from domain.entities.user import User


def map_user_to_dto(user: User) -> UserResponseDTO:
    return UserResponseDTO(id=user.id, name=user.name, email=user.email)


def map_register_user_dto_to_entity(user_dto: RegisterDTO) -> User:
    return User(email=user_dto.email, name=user_dto.name, password=user_dto.password)


def map_user_entity_to_model(user: User) -> UserModel:
    return UserModel(
        id=user.id,
        name=user.name,
        email=user.email,
        password=user.password,
        token=user.token,
        is_verified=user.is_verified,
    )


def map_user_model_to_entity(user_model: UserModel) -> User:
    return User(
        id=user_model.id,
        name=user_model.name,
        email=user_model.email,
        token=user_model.token,
        password=user_model.password,
        is_verified=user_model.is_verified,
    )
