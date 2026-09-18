import os

from fastapi import Depends
from sqlalchemy.orm import Session

from application.interfaces.password_hasher import PasswordHasher
from application.interfaces.token_generator import TokenGenerator
from application.interfaces.email_sender import EmailSender
from infrastructure.security.jwt_token_generator import JwtTokenGenerator
from infrastructure.security.password_hasher_impl import PasswordHasherImpl
from infrastructure.services.email_service import MailtrapEmailSender
from domain.repositories.user_repository import UserRepository
from infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from infrastructure.db.database import get_db


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
    return JwtTokenGenerator(
        secret_key=os.getenv("SECRET_KEY", "change-me-in-prod"),
        algorithm=os.getenv("ALGORITHM", "HS256"),
        expire_minutes=int(os.getenv("TOKEN_EXPIRE_MINUTES", "1440"))
    )