import os
from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from application.interfaces.password_hasher import PasswordHasher
from application.interfaces.token_generator import TokenGenerator
from application.interfaces.email_sender import EmailSender
from domain.entities.user import User
from infrastructure.repositories.user_project_link_repository_impl import UserProjectLinkRepositoryImpl
from domain.repositories.column_repository import ColumnRepository
from domain.repositories.user_project_link_repository import UserProjectLinkRepository
from infrastructure.repositories.column_repository_impl import ColumnRepositoryImpl
from domain.repositories.project_repository import ProjectRepository
from infrastructure.repositories.project_repository_impl import ProjectRepositoryImpl
from domain.utils.constants import Constants
from infrastructure.security.jwt_token_generator import JwtTokenGenerator
from infrastructure.security.password_hasher_impl import PasswordHasherImpl
from infrastructure.services.email_service import MailtrapEmailSender
from domain.repositories.user_repository import UserRepository
from infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from infrastructure.db.database import get_db

security_scheme = HTTPBearer(auto_error=False)

Token = Annotated[Optional[HTTPAuthorizationCredentials], Depends(security_scheme)]

def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepositoryImpl(db)

def get_project_repository(db: Session = Depends(get_db)) -> ProjectRepository:
    return ProjectRepositoryImpl(db)

def get_column_repository(db: Session = Depends(get_db)) -> ColumnRepository:
    return ColumnRepositoryImpl(db)

def get_user_project_link_repository(db: Session = Depends(get_db)) -> UserProjectLinkRepository:
    return UserProjectLinkRepositoryImpl(db)

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

def get_current_user(token: Token, token_generator: TokenGenerator = Depends(get_token_generator), repository: UserRepository = Depends(get_user_repository)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=Constants.TOKEN_INVALID,
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = token_generator.decode_token(token.credentials)
        user_id: str = payload.get("id")
    except:
        raise credentials_exception

    if not user_id:
        raise credentials_exception

    user = repository.get_by_id(user_id)

    if not user:
        raise credentials_exception

    return user

CurrentUser = Annotated[User, Depends(get_current_user)]
TokenGeneratorDep = Annotated[TokenGenerator, Depends(get_token_generator)]
PasswordHasherDep = Annotated[PasswordHasher, Depends(get_password_hasher)]
EmailSenderDep = Annotated[EmailSender, Depends(get_email_sender)]

UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]
ProjectRepositoryDep = Annotated[ProjectRepository, Depends(get_project_repository)]
ColumnRepositoryDep = Annotated[ColumnRepository, Depends(get_column_repository)]
UserProjectLinkRepositoryDep = Annotated[UserProjectLinkRepository, Depends(get_user_project_link_repository)]

    