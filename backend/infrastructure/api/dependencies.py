import os
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from application.interfaces.password_hasher import PasswordHasher
from application.interfaces.token_generator import TokenGenerator
from application.interfaces.email_sender import EmailSender
from domain.exceptions.invalid_credentials_exception import InvalidCredentialsException
from domain.utils.constants import Constants
from infrastructure.schemas.user_schema import UserResponseDTO
from infrastructure.security.jwt_token_generator import JwtTokenGenerator
from infrastructure.security.password_hasher_impl import PasswordHasherImpl
from infrastructure.services.email_service import MailtrapEmailSender
from domain.repositories.user_repository import UserRepository
from infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from infrastructure.db.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

Token = Annotated[str, Depends(oauth2_scheme)]

def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepositoryImpl(db)

def get_password_hasher() -> PasswordHasher:
    return PasswordHasherImpl()

def get_email_sender() -> EmailSender:    
    return MailtrapEmailSender(
        host=os.getenv("MAILTRAP_HOST"),
        port=int(os.getenv("MAILTRAP_PORT")),
        username=os.getenv("MAILTRAP_USER"),
        password=os.getenv("MAILTRAP_PASS"),
        from_email="no-reply@chambeapp.com"
    )

def get_token_generator() -> TokenGenerator:
    return JwtTokenGenerator()

def get_current_user(token: Token, token_generator: TokenGenerator = Depends(get_token_generator), repository: UserRepository = Depends(get_user_repository)) -> UserResponseDTO:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=Constants.TOKEN_INVALID,
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = token_generator.decode_token(token)
        user_id: str = payload.get("id")
    except:
        raise credentials_exception

    if not user_id:
        raise credentials_exception

    user = repository.get_by_id(user_id)

    if not user:
        raise credentials_exception

    return user

    