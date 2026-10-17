from mockito import verify, when, ANY

import pytest

from application.interfaces.password_hasher import PasswordHasher
from application.interfaces.token_generator import TokenGenerator
from application.use_cases.auth.login import LoginUseCase
from infrastructure.schemas.auth_schema import LoginRequestDTO
from domain.exceptions.unverified_account_exception import UnverifiedAccountException
from domain.exceptions.invalid_credentials_exception import InvalidCredentialsException
from domain.utils.constants import Constants
from domain.entities.user import User
from domain.repositories.user_repository import UserRepository


class TestLoginUseCase:
    @pytest.fixture
    def input_user(self) -> LoginRequestDTO:
        user = LoginRequestDTO(
            email="test@email.com",
            password="password",
        )
        return user

    @pytest.fixture
    def expect_user(self) -> User:
        user = User(
            name="test",
            email="test@email.com",
            password="hashed_password",
            is_verified=True,
            token="fake.token",
        )
        return user

    def test_login_succesfully(
        self,
        login_use_case: LoginUseCase,
        mock_repository: UserRepository,
        mock_password_hasher: PasswordHasher,
        mock_token_generator: TokenGenerator,
        input_user: LoginRequestDTO,
        expect_user: User,
    ):

        when(mock_repository).get_by_email(input_user.email).thenReturn(expect_user)
        when(mock_password_hasher).verify(input_user.password, expect_user.password).thenReturn(
            True
        )
        when(mock_token_generator).generate_token(ANY({})).thenReturn(ANY(str))

        token, user = login_use_case.execute(email=input_user.email, password=input_user.password)

        assert token is not None
        assert user == expect_user

        verify(mock_repository).get_by_email(expect_user.email)
        verify(mock_password_hasher).verify(input_user.password, expect_user.password)
        verify(mock_token_generator).generate_token(ANY({}))

    def test_login_not_user_found(
        self, login_use_case, mock_repository: UserRepository, input_user: LoginRequestDTO
    ):

        when(mock_repository).get_by_email(input_user.email).thenReturn(None)

        with pytest.raises(InvalidCredentialsException, match=Constants.INVALID_CREDENTIALS):
            token, user = login_use_case.execute(
                email=input_user.email, password=input_user.password
            )

        verify(mock_repository).get_by_email(input_user.email)

    def test_login_wrong_password(
        self,
        login_use_case,
        mock_repository: UserRepository,
        mock_password_hasher: PasswordHasher,
        input_user: LoginRequestDTO,
        expect_user: User,
    ):

        when(mock_repository).get_by_email(input_user.email).thenReturn(expect_user)
        when(mock_password_hasher).verify(input_user.password, expect_user.password).thenReturn(
            False
        )

        with pytest.raises(InvalidCredentialsException, match=Constants.INVALID_CREDENTIALS):
            token, user = login_use_case.execute(
                email=input_user.email, password=input_user.password
            )

        verify(mock_repository).get_by_email(input_user.email)
        verify(mock_password_hasher).verify(input_user.password, expect_user.password)

    def test_login_user_not_verified(
        self,
        login_use_case,
        mock_repository: UserRepository,
        mock_password_hasher: PasswordHasher,
        input_user: LoginRequestDTO,
        expect_user: User,
    ):
        expect_user.is_verified = False

        when(mock_repository).get_by_email(input_user.email).thenReturn(expect_user)
        when(mock_password_hasher).verify(input_user.password, expect_user.password).thenReturn(
            True
        )

        with pytest.raises(UnverifiedAccountException, match=Constants.UNVERIFIED_ACCOUNT):
            token, user = login_use_case.execute(
                email=input_user.email, password=input_user.password
            )

        verify(mock_repository).get_by_email(input_user.email)
        verify(mock_password_hasher).verify(input_user.password, expect_user.password)
