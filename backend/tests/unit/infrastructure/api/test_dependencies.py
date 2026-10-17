from fastapi import HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from mockito import mock, verify, when, ANY

import pytest

from application.interfaces.token_generator import TokenGenerator
from domain.entities.user import User
from domain.repositories.user_repository import UserRepository
from domain.utils.constants import Constants
from infrastructure.api.dependencies import get_current_user


def _credentials(token: str = "valid-token") -> HTTPAuthorizationCredentials:
    return HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)


class TestGetCurrentUser:
    @pytest.fixture
    def mock_token_generator(self) -> TokenGenerator:
        return mock(TokenGenerator)

    @pytest.fixture
    def mock_user_repository(self) -> UserRepository:
        return mock(UserRepository)

    @pytest.fixture
    def user(self) -> User:
        return User(
            id="user-1",
            name="Test",
            email="test@test.com",
            password="hashed",
            is_verified=True,
        )

    def test_returns_user_for_valid_token(
        self,
        mock_token_generator: TokenGenerator,
        mock_user_repository: UserRepository,
        user: User,
    ):
        when(mock_token_generator).decode_token("valid-token").thenReturn({"id": "user-1"})
        when(mock_user_repository).get_by_id("user-1").thenReturn(user)

        result = get_current_user(_credentials(), mock_token_generator, mock_user_repository)

        assert result == user
        verify(mock_token_generator).decode_token("valid-token")
        verify(mock_user_repository).get_by_id("user-1")

    def test_raises_401_when_token_cannot_be_decoded(
        self,
        mock_token_generator: TokenGenerator,
        mock_user_repository: UserRepository,
    ):
        when(mock_token_generator).decode_token("bad-token").thenRaise(Exception("invalid"))

        with pytest.raises(HTTPException) as exc:
            get_current_user(_credentials("bad-token"), mock_token_generator, mock_user_repository)

        assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
        assert exc.value.detail == Constants.TOKEN_INVALID
        assert exc.value.headers == {"WWW-Authenticate": "Bearer"}
        verify(mock_user_repository, times=0).get_by_id(ANY)

    def test_raises_401_when_payload_has_no_id(
        self,
        mock_token_generator: TokenGenerator,
        mock_user_repository: UserRepository,
    ):
        when(mock_token_generator).decode_token("valid-token").thenReturn({})

        with pytest.raises(HTTPException) as exc:
            get_current_user(_credentials(), mock_token_generator, mock_user_repository)

        assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
        verify(mock_user_repository, times=0).get_by_id(ANY)

    def test_raises_401_when_user_not_found(
        self,
        mock_token_generator: TokenGenerator,
        mock_user_repository: UserRepository,
    ):
        when(mock_token_generator).decode_token("valid-token").thenReturn({"id": "ghost"})
        when(mock_user_repository).get_by_id("ghost").thenReturn(None)

        with pytest.raises(HTTPException) as exc:
            get_current_user(_credentials(), mock_token_generator, mock_user_repository)

        assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
        verify(mock_user_repository).get_by_id("ghost")

    def test_raises_401_when_token_missing(
        self,
        mock_token_generator: TokenGenerator,
        mock_user_repository: UserRepository,
    ):
        with pytest.raises(HTTPException) as exc:
            get_current_user(None, mock_token_generator, mock_user_repository)

        assert exc.value.status_code == status.HTTP_401_UNAUTHORIZED
        verify(mock_token_generator, times=0).decode_token(ANY)
