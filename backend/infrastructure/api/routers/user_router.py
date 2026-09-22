from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status, Depends
from application.use_cases.users.get_user import GetUserUseCase
from application.interfaces.password_hasher import PasswordHasher
from application.use_cases.users.update_profile_user import UpdateUserUseCase
from application.use_cases.users.change_password_user import ChangePasswordUseCase
from domain.repositories.user_repository import UserRepository
from domain.exceptions.not_found_exception import NotFoundException
from domain.exceptions.invalid_credentials_exception import InvalidCredentialsException
from domain.utils.constants import Constants
from infrastructure.api.dependencies import get_user_repository, get_password_hasher
from infrastructure.schemas.user_schema import ChangePasswordUserDTO, UpdateProfileUserDTO, UserResponseDTO
from infrastructure.schemas.pagination_schema import PaginatedResponseDTO


router = APIRouter(prefix='/users', tags=['Users'])

@router.get('/', status_code=status.HTTP_200_OK, response_model=PaginatedResponseDTO[UserResponseDTO])
async def get_users(
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
            detail=Constants.UNEXPECTED_ERROR + str(e)
        )

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=UserResponseDTO)
def get_user(id: str, respository: UserRepository = Depends(get_user_repository)):
    try:
        use_case = GetUserUseCase(respository)
        user = use_case.execute_by_id(id)
        return UserResponseDTO.model_validate(user)
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=Constants.UNEXPECTED_ERROR + str(e)
        )

@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=UserResponseDTO)
def update_profile_user(id: str, user_data: UpdateProfileUserDTO, repository: UserRepository = Depends(get_user_repository)):
    try:
        use_case = UpdateUserUseCase(repository)
        user = use_case.execute(
            id, user_data.name
        )
        return UserResponseDTO.model_validate(user)
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=Constants.UNEXPECTED_ERROR + str(e)
        )

@router.put('/me/password', status_code=status.HTTP_204_NO_CONTENT)
def change_password_user(id: str, user_data: ChangePasswordUserDTO, repository: UserRepository = Depends(get_user_repository), password_hasher: PasswordHasher = Depends(get_password_hasher)):
    try:
        use_case = ChangePasswordUseCase(repository, password_hasher)
        use_case.execute(
            user_id=id, 
            old_password=user_data.old_password,
            new_password=user_data.new_password
        )
        return
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= str(e)
        )
    except InvalidCredentialsException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail= str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=Constants.UNEXPECTED_ERROR + str(e)
        )

