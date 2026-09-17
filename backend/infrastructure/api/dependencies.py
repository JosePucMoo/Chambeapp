from fastapi import Depends
from sqlalchemy.orm import Session

from application.interfaces.password_hasher import PasswordHasher
from infrastructure.security.password_hasher_impl import PasswordHasherImpl
from domain.repositories.user_repository import UserRepository
from infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from infrastructure.db.database import get_db


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepositoryImpl(db)

def get_password_hasher() -> PasswordHasher:
    return PasswordHasherImpl()