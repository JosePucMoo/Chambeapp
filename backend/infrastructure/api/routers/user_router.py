from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status, Depends
from application.use_cases.users.create_user import CreateUserUseCase
from application.use_cases.users.get_user import GetUserUseCase
from application.interfaces.password_hasher import PasswordHasher
from domain.exceptions.resource_alredy_exists_exception import ResourceAlreadyExistsException
from domain.repositories.user_repository import UserRepository
from domain.exceptions.cannot_create_exception import CannotCreateException
from domain.utils.constants import UNEXPECTED_ERROR
from infrastructure.api.dependencies import get_user_repository, get_password_hasher
from infrastructure.mappers.user_mappers import map_create_user_dto_to_entity
from infrastructure.schemas.user_schema import CreateUserDTO, UserResponseDTO
from infrastructure.schemas.pagination_schema import PaginatedResponseDTO


router = APIRouter(prefix='/users', tags=['Users'])

@router.get('/', status_code=status.HTTP_200_OK, response_model=PaginatedResponseDTO[UserResponseDTO])
async def get_user(
    page: Annotated[int, Query(ge=1)] = 1, 
    size: Annotated[int, Query(ge=1, le=100)] = 10, 
    repository: UserRepository = Depends(get_user_repository)
):
    try:
        use_case = GetUserUseCase(repository)
        (users, total_count) = use_case.execute_all(page, size)
        return PaginatedResponseDTO.create(
            data=[UserResponseDTO.model_validate(user) for user in users],
            size=size,
            page=page,
            total_count=total_count
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=UNEXPECTED_ERROR + str(e)
        )


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserResponseDTO)
async def create_user(user_data: CreateUserDTO, repository: UserRepository = Depends(get_user_repository), password_hasher: PasswordHasher = Depends(get_password_hasher)) -> UserResponseDTO:
    try:
        use_case = CreateUserUseCase(repository, password_hasher)
        user = use_case.execute(
            map_create_user_dto_to_entity(user_data)
        )
        return UserResponseDTO.model_validate(user)
    except CannotCreateException and ResourceAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=UNEXPECTED_ERROR + str(e)
        )

