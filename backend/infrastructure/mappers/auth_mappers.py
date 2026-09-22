
from domain.entities.user import User
from infrastructure.schemas.auth_schema import UserResponseDTO


def map_user_to_dto(user: User) -> UserResponseDTO:
    return UserResponseDTO(
        id=user.id,
        name=user.name,
        email=user.email
    )