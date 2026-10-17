from mockito import verify, when

import pytest

from application.use_cases.auth.verify_token import VerifyTokenUseCase
from domain.entities.user import User
from domain.exceptions.invalid_token_exception import InvalidTokenException
from domain.exceptions.unverified_account_exception import UnverifiedAccountException
from domain.repositories.user_repository import UserRepository
from domain.utils.constants import Constants


class TestVerifyTokenUseCase:
    @pytest.fixture
    def input_token(self) -> str:
        return "reset_token"

    def test_valid_token(
        self,
        verify_token_use_case: VerifyTokenUseCase,
        mock_repository: UserRepository,
        input_token: str,
    ):
        user = User(
            name="test",
            email="test@email.com",
            password="hashed_password",
            token=input_token,
            is_verified=True,
        )
        when(mock_repository).get_by_token(input_token).thenReturn(user)

        response = verify_token_use_case.execute(input_token)

        assert response is None
        verify(mock_repository).get_by_token(input_token)

    def test_token_not_found(
        self,
        verify_token_use_case: VerifyTokenUseCase,
        mock_repository: UserRepository,
        input_token: str,
    ):
        when(mock_repository).get_by_token(input_token).thenReturn(None)

        with pytest.raises(InvalidTokenException, match=Constants.TOKEN_INVALID):
            verify_token_use_case.execute(input_token)

        verify(mock_repository).get_by_token(input_token)

    def test_account_not_verified(
        self,
        verify_token_use_case: VerifyTokenUseCase,
        mock_repository: UserRepository,
        input_token: str,
    ):
        user = User(
            name="test",
            email="test@email.com",
            password="hashed_password",
            token=input_token,
            is_verified=False,
        )
        when(mock_repository).get_by_token(input_token).thenReturn(user)

        with pytest.raises(UnverifiedAccountException, match=Constants.UNVERIFIED_ACCOUNT):
            verify_token_use_case.execute(input_token)

        verify(mock_repository).get_by_token(input_token)
