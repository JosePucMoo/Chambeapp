from mockito import verify, when, ANY

import pytest

from application.interfaces.password_hasher import PasswordHasher
from application.use_cases.auth.reset_password import ResetPasswordUseCase
from domain.entities.user import User
from domain.exceptions.invalid_token_exception import InvalidTokenException
from domain.exceptions.unverified_account_exception import UnverifiedAccountException
from domain.repositories.user_repository import UserRepository
from domain.utils.constants import Constants


class TestResetPasswordUseCase:
    @pytest.fixture
    def input_token(self) -> str:
        return "reset_token"

    @pytest.fixture
    def new_password(self) -> str:
        return "new_password"

    def test_reset_succesfully(
        self,
        reset_password_use_case: ResetPasswordUseCase,
        mock_repository: UserRepository,
        mock_password_hasher: PasswordHasher,
        input_token: str,
        new_password: str,
    ):
        user = User(
            name="test",
            email="test@email.com",
            password="old_hashed_password",
            token=input_token,
            is_verified=True,
        )
        when(mock_repository).get_by_token(input_token).thenReturn(user)
        when(mock_password_hasher).hash(new_password).thenReturn("new_hashed_password")
        when(mock_repository).update(ANY(User)).thenReturn(user)

        response = reset_password_use_case.execute(token=input_token, new_password=new_password)

        assert response is None
        assert user.password == "new_hashed_password"
        assert user.token is None

        verify(mock_repository).get_by_token(input_token)
        verify(mock_password_hasher).hash(new_password)
        verify(mock_repository).update(user)

    def test_invalid_token(
        self,
        reset_password_use_case: ResetPasswordUseCase,
        mock_repository: UserRepository,
        mock_password_hasher: PasswordHasher,
        input_token: str,
    ):
        when(mock_repository).get_by_token(input_token).thenReturn(None)

        with pytest.raises(InvalidTokenException, match=Constants.MISSING_TOKEN):
            reset_password_use_case.execute(token=input_token, new_password="new_password")

        verify(mock_repository).get_by_token(input_token)
        verify(mock_password_hasher, times=0).hash(ANY(str))
        verify(mock_repository, times=0).update(ANY(User))

    def test_account_not_verified(
        self,
        reset_password_use_case: ResetPasswordUseCase,
        mock_repository: UserRepository,
        mock_password_hasher: PasswordHasher,
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
            reset_password_use_case.execute(token=input_token, new_password="new_password")

        verify(mock_repository).get_by_token(input_token)
        verify(mock_password_hasher, times=0).hash(ANY(str))
        verify(mock_repository, times=0).update(ANY(User))
