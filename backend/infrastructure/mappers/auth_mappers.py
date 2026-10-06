from domain.entities.user import User
from infrastructure.schemas.auth_schema import RegisterDTO, UserResponseDTO


def map_user_to_dto(user: User) -> UserResponseDTO:
    return UserResponseDTO(id=user.id, name=user.name, email=user.email)


def map_register_user_dto_to_entity(user_dto: RegisterDTO) -> User:
    return User(id=None, email=user_dto.email, name=user_dto.name, password=user_dto.password)
