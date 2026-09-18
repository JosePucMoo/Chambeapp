from domain.exceptions.invalid_token_exception import InvalidTokenException
from domain.exceptions.unverified_account_exception import UnverifiedAccountException
from domain.repositories.user_repository import UserRepository
from application.interfaces.password_hasher import PasswordHasher

class ResetPasswordUseCase:
    def __init__(self, repository: UserRepository, password_hasher: PasswordHasher):
        self.repository = repository
        self.password_hasher = password_hasher

    def execute(self, token: str, new_password: str) -> None:
        user = self.repository.get_by_token(token)
        
        if not user:
            raise InvalidTokenException("El enlace de recuperación es inválido o ha expirado.")

        if not user.is_verified:
            raise UnverifiedAccountException("Por favor verifica tu correo electrónico.")

        new_hashed_password = self.password_hasher.hash(new_password)
        
        user.change_password(new_hashed_password)
        
        user.clear_password_reset_token()
        
        self.user_repo.update(user)