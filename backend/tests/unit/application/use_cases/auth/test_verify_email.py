from mockito import verify, when, ANY

import pytest

from application.use_cases.auth.verify_email import VerifyEmailUseCase
from domain.entities.user import User
from domain.exceptions.invalid_token_exception import InvalidTokenException
from domain.repositories.user_repository import UserRepository
from domain.utils.constants import Constants


class TestVerifyEmailUseCase:
    @pytest.fixture
    def input_token(self) -> str:
        return "verification_token"

    @pytest.fixture
    def expect_user(self) -> User:
        return User(
            name="test",
            email="test@email.com",
            password="hashed_password",
            token="verification_token",
            is_verified=False,
        )

    def test_verify_succesfully(
        self,
        verify_email_use_case: VerifyEmailUseCase,
        mock_repository: UserRepository,
        input_token: str,
        expect_user: User,
    ):
        when(mock_repository).get_by_token(input_token).thenReturn(expect_user)
        when(mock_repository).update(ANY(User)).thenReturn(expect_user)

        response = verify_email_use_case.execute(input_token)

        assert response is None
        assert expect_user.is_verified is True
        assert expect_user.token is None

        verify(mock_repository).get_by_token(input_token)
        verify(mock_repository).update(expect_user)

    def test_invalid_token(
        self,
        verify_email_use_case: VerifyEmailUseCase,
        mock_repository: UserRepository,
        input_token: str,
    ):
        when(mock_repository).get_by_token(input_token).thenReturn(None)

        with pytest.raises(InvalidTokenException, match=Constants.LINK_EXPIRED):
            verify_email_use_case.execute(input_token)

        verify(mock_repository).get_by_token(input_token)
        verify(mock_repository, times=0).update(ANY(User))
