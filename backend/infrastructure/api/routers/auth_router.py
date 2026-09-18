from fastapi import APIRouter, Depends, HTTPException, status

from application.interfaces.password_hasher import PasswordHasher
from application.interfaces.email_sender import EmailSender
from application.use_cases.users.auth.register_user import RegisterUserUseCase
from application.use_cases.users.auth.verify_email import VerifyEmailUseCase
from domain.exceptions.cannot_create_exception import CannotCreateException
from domain.exceptions.resource_alredy_exists_exception import ResourceAlreadyExistsException
from domain.exceptions.invalid_token_exception import InvalidTokenException
from domain.repositories.user_repository import UserRepository
from domain.utils.constants import UNEXPECTED_ERROR
from infrastructure.api.dependencies import get_email_sender, get_password_hasher, get_user_repository
from infrastructure.mappers.user_mappers import map_create_user_dto_to_entity
from infrastructure.schemas.user_schema import UserResponseDTO
from infrastructure.schemas.auth_schema import (
    RegisterDTO, 
    RegisterResponseDTO, 
)

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=RegisterResponseDTO)
async def register(user_data: RegisterDTO, repository: UserRepository = Depends(get_user_repository), password_hasher: PasswordHasher = Depends(get_password_hasher), email_sender: EmailSender = Depends(get_email_sender)) -> UserResponseDTO:
    try:
        use_case = RegisterUserUseCase(repository, password_hasher, email_sender)
        user = use_case.execute(
            map_create_user_dto_to_entity(user_data)
        )
        return {
            "message": "Registro exitoso. Por favor, revisa tu bandeja de entrada para verificar tu cuenta.",
            "email": user.email
        }
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

@router.post("/verify-email/{token}", status_code=status.HTTP_200_OK)
def verify_email(
    token: str,
    repository: UserRepository = Depends(get_user_repository)
):
    try:
        use_case = VerifyEmailUseCase(repository)
        use_case.execute(token)
        return {"message": "Cuenta verificada exitosamente. Ya puedes iniciar sesión."}
    except InvalidTokenException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=UNEXPECTED_ERROR + str(e)
        )