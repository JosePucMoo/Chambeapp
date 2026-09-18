from fastapi import APIRouter, Depends, HTTPException, status

from application.interfaces.password_hasher import PasswordHasher
from application.interfaces.email_sender import EmailSender
from application.use_cases.auth.register_user import RegisterUserUseCase
from application.use_cases.auth.verify_email import VerifyEmailUseCase
from application.use_cases.auth.request_password_reset import RequestPasswordResetUseCase
from application.use_cases.auth.reset_password import ResetPasswordUseCase
from application.interfaces.token_generator import TokenGenerator
from application.use_cases.auth.login import LoginUseCase
from domain.exceptions.invalid_credentials_exception import InvalidCredentialsException
from domain.exceptions.unverified_account_exception import UnverifiedAccountException
from domain.exceptions.cannot_create_exception import CannotCreateException
from domain.exceptions.resource_alredy_exists_exception import ResourceAlreadyExistsException
from domain.exceptions.invalid_token_exception import InvalidTokenException
from domain.repositories.user_repository import UserRepository
from domain.utils.constants import UNEXPECTED_ERROR
from infrastructure.api.dependencies import get_email_sender, get_password_hasher, get_token_generator, get_user_repository
from infrastructure.mappers.user_mappers import map_create_user_dto_to_entity
from infrastructure.schemas.user_schema import UserResponseDTO
from infrastructure.schemas.auth_schema import (
    RegisterDTO, 
    LoginDTO, 
    RegisterResponseDTO, 
    TokenResponseDTO,
    ForgotPasswordDTO,
    ResetPasswordDTO
)

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=RegisterResponseDTO)
async def register(user_data: RegisterDTO, repository: UserRepository = Depends(get_user_repository), password_hasher: PasswordHasher = Depends(get_password_hasher), email_sender: EmailSender = Depends(get_email_sender)) -> UserResponseDTO:
    try:
        use_case = RegisterUserUseCase(repository, password_hasher, email_sender)
        user = use_case.execute(
            map_create_user_dto_to_entity(user_data)
        )
        return RegisterResponseDTO(
            message="Registro exitoso. Por favor, revisa tu bandeja de entrada para verificar tu cuenta.",
            email=user.email
        ) 
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

@router.post("/login", status_code=status.HTTP_200_OK, response_model=TokenResponseDTO)
def login(
    login_dto: LoginDTO, 
    repository: UserRepository = Depends(get_user_repository),
    token_generator: TokenGenerator = Depends(get_token_generator),
    password_hasher: PasswordHasher = Depends(get_password_hasher)
):
    try:
        use_case = LoginUseCase(repository=repository, password_hasher=password_hasher, token_generator=token_generator)
        token = use_case.execute(email=login_dto.email, password=login_dto.password)
        
        return TokenResponseDTO(access_token=token)
    except UnverifiedAccountException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except InvalidCredentialsException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=UNEXPECTED_ERROR + str(e)
        )

@router.post("/forgot-password", status_code=status.HTTP_200_OK)
def forgot_password(
    forgot_password_dto: ForgotPasswordDTO, 
    repository= Depends(get_user_repository),
    email_sender = Depends(get_email_sender)
):
    use_case = RequestPasswordResetUseCase(repository=repository, email_sender=email_sender)
    use_case.execute(email=forgot_password_dto.email)
    
    return {
        "message": "Recibirás un enlace con instrucciones"
    }

@router.post("/reset-password/{token}", status_code=status.HTTP_204_NO_CONTENT)
def reset_password(
    token: str,
    reset_password_dto: ResetPasswordDTO, 
    repository: UserRepository = Depends(get_user_repository),
    password_hasher: EmailSender = Depends(get_password_hasher)
):
    try:
        use_case = ResetPasswordUseCase(repository=repository, password_hasher=password_hasher)
        use_case.execute(token=token, new_password=reset_password_dto.new_password)
        return 
    except InvalidCredentialsException as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail=str(e),
                headers={"WWW-Authenticate": "Bearer"},
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=UNEXPECTED_ERROR + str(e)
        )

