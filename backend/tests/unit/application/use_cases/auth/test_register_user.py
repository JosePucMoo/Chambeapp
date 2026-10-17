from mockito import verify, when, ANY
import pytest

from application.interfaces.email_sender import EmailSender
from application.interfaces.password_hasher import PasswordHasher
from application.use_cases.auth.register_user import RegisterUserUseCase
from domain.exceptions.cannot_create_exception import CannotCreateException
from domain.exceptions.resource_alredy_exists_exception import ResourceAlreadyExistsException
from domain.utils.constants import Constants
from infrastructure.schemas.auth_schema import RegisterDTO
from domain.entities.user import User
from domain.repositories.user_repository import UserRepository


class TestRegisterUserUseCase:
    @pytest.fixture
    def input_user(self) -> RegisterDTO:
        user = RegisterDTO(
            name="test", email="test@email.com", password="password", confirm_password="password"
        )
        return user

    @pytest.fixture
    def expect_user(self) -> User:
        user = User(
            name="test",
            email="test@email.com",
            password="hashed_password",
            token="secrets_token",
            is_verified=False,
        )
        return user

    def test_register_succesfully(
        self,
        register_user_use_case: RegisterUserUseCase,
        mock_repository: UserRepository,
        mock_password_hasher: PasswordHasher,
        mock_email_sender: EmailSender,
        input_user: RegisterDTO,
        expect_user: User,
    ):
        when(mock_repository).get_by_email(input_user.email).thenReturn(None)

        when(mock_repository).create(ANY(User)).thenReturn(expect_user)

        when(mock_password_hasher).hash(input_user.password).thenReturn(expect_user.password)

        when(mock_email_sender).send_verification_email(
            to_email=expect_user.email, verification_token=ANY(str)
        ).thenReturn(None)

        created_user = register_user_use_case.execute(input_user)

        assert created_user.id == expect_user.id
        assert created_user.is_verified is False
        assert created_user.token is not None

        verify(mock_repository).get_by_email(input_user.email)
        verify(mock_password_hasher).hash(input_user.password)
        verify(mock_email_sender).send_verification_email(
            to_email=input_user.email, verification_token=ANY(str)
        )
        verify(mock_repository).create(ANY(User))

    def test_email_already_exist(
        self,
        register_user_use_case: RegisterUserUseCase,
        mock_repository: UserRepository,
        input_user: RegisterDTO,
        expect_user: User,
    ):
        when(mock_repository).get_by_email(input_user.email).thenReturn(expect_user)

        with pytest.raises(ResourceAlreadyExistsException, match=Constants.EMAIL_ALREADY_EXISTS):
            register_user_use_case.execute(input_user)

        verify(mock_repository).get_by_email(input_user.email)

    def test_cannot_create_user(
        self,
        register_user_use_case: RegisterUserUseCase,
        mock_repository: UserRepository,
        mock_password_hasher: PasswordHasher,
        input_user: RegisterDTO,
    ):
        when(mock_repository).get_by_email(input_user.email).thenReturn(None)
        when(mock_repository).create(ANY(User)).thenReturn(None)
        when(mock_password_hasher).hash(input_user.password).thenReturn(ANY(str))

        with pytest.raises(CannotCreateException, match=Constants.USER_NOT_CREATED):
            register_user_use_case.execute(input_user)

        verify(mock_repository).get_by_email(input_user.email)
        verify(mock_repository).create(ANY(User))
