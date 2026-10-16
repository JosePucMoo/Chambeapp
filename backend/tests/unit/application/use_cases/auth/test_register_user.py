from mockito import verify, when, ANY
import pytest

from application.interfaces.email_sender import EmailSender
from application.interfaces.password_hasher import PasswordHasher
from application.use_cases.auth.register_user import RegisterUserUseCase
from domain.entities.user import User
from domain.repositories.user_repository import UserRepository


class TestRegisterUserUseCase:
    
    @pytest.fixture
    def fake_user_to_register(self) -> User:
        user = User(
            name="test",
            email="test@email.com",
            password="hashed_password",
        )
        return user
    
    @pytest.fixture
    def fake_registered_user(self) -> User:
        user = User(
            id="idxd",
            name="test",
            email="test@email.com",
            password="hashed_password",
            token="secrets.token_urlsafe(32)",
            is_verified=False
        )
        return user
    
    def test_register_succesfully(
        self,
        register_user_use_case: RegisterUserUseCase,
        mock_repository: UserRepository,
        mock_password_hasher: PasswordHasher,
        mock_email_sender: EmailSender,
        fake_user_to_register: User,
        fake_registered_user: User
    ):        
        when(mock_repository).get_by_email(fake_user_to_register.email).thenReturn(None)
        
        when(mock_repository).create(ANY(User)).thenReturn(fake_registered_user)
        
        when(mock_password_hasher).hash(fake_user_to_register.password).thenReturn(fake_registered_user.password)
        
        when(mock_email_sender).send_verification_email(
            to_email=fake_registered_user.email, 
            verification_token=ANY(str)).thenReturn(None)
        
        created_user = register_user_use_case.execute(fake_user_to_register)
        
        assert created_user.token != fake_user_to_register.token
        assert created_user.is_verified == False
        
        verify(mock_repository, times=1).get_by_email(fake_user_to_register.email)
        verify(mock_repository, times=1).create(ANY(User))
        verify(mock_password_hasher, times=1).hash(fake_user_to_register.password)
        verify(mock_email_sender, times=1).send_verification_email(
            to_email=fake_user_to_register.email, verification_token = ANY(str))
        
        
        
        