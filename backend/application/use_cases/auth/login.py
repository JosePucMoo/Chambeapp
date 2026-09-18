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

    def execute(self, email: str, password: str) -> str:
        user = self.repository.get_by_email(email.lower())

        error_msg = "Correo electrónico o contraseña incorrectos."
        if not user:
            raise InvalidCredentialsException(error_msg)

        if not self.password_hasher.verify(password, user.hashed_password):
            raise InvalidCredentialsException(error_msg)
            
        if not user.is_verified:
            raise UnverifiedAccountException("Por favor verifica tu correo electrónico antes de iniciar sesión.")

        payload = {
            "sub": str(user.id),
            "email": user.email
        }

        return self.token_generator.generate_token(payload)