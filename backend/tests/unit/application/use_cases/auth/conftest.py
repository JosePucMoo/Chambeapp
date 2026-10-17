from mockito import mock
import pytest

from application.interfaces.password_hasher import PasswordHasher
from application.interfaces.token_generator import TokenGenerator
from application.use_cases.auth.login import LoginUseCase
from application.use_cases.auth.register_user import RegisterUserUseCase
from application.interfaces.email_sender import EmailSender
from application.use_cases.auth.request_password_reset import RequestPasswordResetUseCase
from application.use_cases.auth.reset_password import ResetPasswordUseCase
from application.use_cases.auth.verify_email import VerifyEmailUseCase
from application.use_cases.auth.verify_token import VerifyTokenUseCase
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
def mock_email_sender() -> EmailSender:
    return mock(EmailSender)


@pytest.fixture
def login_use_case(
    mock_repository: UserRepository,
    mock_password_hasher: PasswordHasher,
    mock_token_generator: TokenGenerator,
) -> LoginUseCase:
    return LoginUseCase(
        repository=mock_repository,
        password_hasher=mock_password_hasher,
        token_generator=mock_token_generator,
    )


@pytest.fixture
def register_user_use_case(
    mock_repository: UserRepository,
    mock_password_hasher: PasswordHasher,
    mock_email_sender: EmailSender,
) -> RegisterUserUseCase:
    return RegisterUserUseCase(
        repository=mock_repository,
        password_hasher=mock_password_hasher,
        email_sender=mock_email_sender,
    )
    
@pytest.fixture
def request_password_reset_use_case(
    mock_repository: UserRepository,
    mock_email_sender: EmailSender,
) -> RequestPasswordResetUseCase:
    return RequestPasswordResetUseCase(
        repository=mock_repository,
        email_sender=mock_email_sender,
    )


@pytest.fixture
def verify_email_use_case(mock_repository: UserRepository) -> VerifyEmailUseCase:
    return VerifyEmailUseCase(repository=mock_repository)


@pytest.fixture
def verify_token_use_case(mock_repository: UserRepository) -> VerifyTokenUseCase:
    return VerifyTokenUseCase(repository=mock_repository)


@pytest.fixture
def reset_password_use_case(
    mock_repository: UserRepository,
    mock_password_hasher: PasswordHasher,
) -> ResetPasswordUseCase:
    return ResetPasswordUseCase(
        repository=mock_repository,
        password_hasher=mock_password_hasher,
    )
