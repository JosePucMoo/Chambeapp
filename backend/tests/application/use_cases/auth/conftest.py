from mockito import mock
import pytest

from application.interfaces.password_hasher import PasswordHasher
from application.interfaces.token_generator import TokenGenerator
from application.use_cases.auth.login import LoginUseCase
from domain.entities.user import User
from domain.repositories.user_repository import UserRepository


@pytest.fixture
def mock_repository() -> UserRepository:
    return mock(UserRepository)

@pytest.fixture
def mock_password_hasher() -> PasswordHasher:
    return mock(PasswordHasher)

@pytest.fixture
def mock_token_generator() -> TokenGenerator:
    return mock(TokenGenerator)

@pytest.fixture
def fake_user() -> User:
    user = User(
        name="test",
        email="test@email.com",
        password="hashed_password",
        is_verified=True,
        token="jwt.fake.token"
    )
    return user

@pytest.fixture
def login_use_case(
    mock_repository: UserRepository,
    mock_password_hasher: PasswordHasher,
    mock_token_generator: TokenGenerator,
    ) -> LoginUseCase:
    return LoginUseCase(
        repository=mock_repository,
        password_hasher=mock_password_hasher,
        token_generator=mock_token_generator
    )