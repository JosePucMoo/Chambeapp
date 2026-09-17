from fastapi import APIRouter, HTTPException, status, Depends
from application.use_cases.users.create_user import CreateUserUseCase
from application.interfaces.password_hasher import PasswordHasher
from domain.exceptions.resource_alredy_exists_exception import ResourceAlreadyExistsException
from domain.repositories.user_repository import UserRepository
from domain.exceptions.cannot_create_exception import CannotCreateException
from domain.utils.constants import UNEXPECTED_ERROR
from infrastructure.api.dependencies import get_user_repository, get_password_hasher
from infrastructure.mappers.user_mappers import map_create_user_dto_to_entity
from infrastructure.schemas.user_schema import CreateUserDTO, UserResponseDTO


router = APIRouter(prefix='/users', tags=['Users'])

@router.get('/')
async def get_user():
    return {
        'message': 'hola'
    }


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

