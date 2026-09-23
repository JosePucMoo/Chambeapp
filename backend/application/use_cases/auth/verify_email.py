from domain.utils.constants import Constants
from domain.exceptions.invalid_token_exception import InvalidTokenException
from domain.repositories.user_repository import UserRepository

class VerifyEmailUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(self, token: str) -> None:
        user = self.repository.get_by_token(token)
        if not user:
            raise InvalidTokenException(Constants.LINK_EXPIRED)

        user.verify_account()

        self.repository.update(user)