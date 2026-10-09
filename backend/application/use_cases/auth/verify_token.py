from domain.exceptions.unverified_account_exception import UnverifiedAccountException
from domain.utils.constants import Constants
from domain.exceptions.invalid_token_exception import InvalidTokenException
from domain.repositories.user_repository import UserRepository


class VerifyTokenUseCase:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def execute(self, token: str):
        user = self.repository.get_by_token(token)

        if not user:
            raise InvalidTokenException(Constants.TOKEN_INVALID)

        if not user.is_verified:
            raise UnverifiedAccountException(Constants.UNVERIFIED_ACCOUNT)

        return
