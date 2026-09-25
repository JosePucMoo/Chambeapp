from infrastructure.mappers.auth_mappers import map_user_to_dto
from domain.entities.user import User
from domain.utils.constants import Constants
from domain.exceptions.invalid_credentials_exception import InvalidCredentialsException
from domain.exceptions.unverified_account_exception import UnverifiedAccountException
from domain.repositories.user_repository import UserRepository
from application.interfaces.password_hasher import PasswordHasher
from application.interfaces.token_generator import TokenGenerator

class LoginUseCase:
    def __init__(
        self, 
        repository: UserRepository, 
        password_hasher: PasswordHasher,
        token_generator: TokenGenerator
    ):
        self.repository = repository
        self.password_hasher = password_hasher
        self.token_generator = token_generator

    def execute(self, email: str, password: str) -> tuple[str, User]:
        user = self.repository.get_by_email(email.lower())

        error_msg = Constants.INVALID_CREDENTIALS
        if not user:
            raise InvalidCredentialsException(error_msg)

        if not self.password_hasher.verify(password, user.hashed_password):
            raise InvalidCredentialsException(error_msg)
            
        if not user.is_verified:
            raise UnverifiedAccountException(Constants.UNVERIFIED_ACCOUNT)

        payload = {
            "id": str(user.id),
        }

        token = self.token_generator.generate_token(payload)

        return [
            token, 
            map_user_to_dto(user)
        ]