

from fastapi import HTTPException

from application.interfaces.password_hasher import PasswordHasher
from domain.entities.user import User
from domain.repositories.user_repository import UserRepository
from domain.exceptions.cannot_create_exception import CannotCreateException
from domain.exceptions.resource_alredy_exists_exception import ResourceAlreadyExistsException


class CreateUserUseCase:
    def __init__(self, repository: UserRepository, password_hasher: PasswordHasher):
        self.repository = repository
        self.password_hasher = password_hasher

    def execute(self, user_data: User) -> User:
        if self.repository.get_by_email(user_data.email):
            raise ResourceAlreadyExistsException("Email ya registrado")

        password_hashed = self.password_hasher.hash(user_data.password)
        user = User(
            name=user_data.name,
            email=user_data.email,
            password=password_hashed
        )
        created_user = self.repository.create(user) 

        if not created_user:
            raise CannotCreateException("No se pudo crear el usuario")

        return created_user