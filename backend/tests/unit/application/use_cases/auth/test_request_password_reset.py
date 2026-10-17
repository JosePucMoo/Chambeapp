
from mockito import verify, when, ANY
import pytest

from application.interfaces.email_sender import EmailSender
from application.use_cases.auth.request_password_reset import RequestPasswordResetUseCase
from domain.entities.user import User
from domain.repositories.user_repository import UserRepository


class TestRequestPasswordResetUseCase:
    
    @pytest.fixture
    def input_email(self) -> str:
        return "test@email.com"
    
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
    
    def test_request_succesfully(
        self,
        request_password_reset_use_case: RequestPasswordResetUseCase,
        mock_repository: UserRepository,
        mock_email_sender: EmailSender,
        input_email: str,
        expect_user: User
    ):
        when(mock_repository).get_by_email(input_email).thenReturn(expect_user) 
        when(mock_repository).update(ANY(User)).thenReturn(ANY(User))
        when(mock_email_sender).send_password_reset_email(to_email=expect_user.email, verification_token=ANY(str)).thenReturn(None)
        
        response = request_password_reset_use_case.execute(input_email)
        
        assert response is None
        
        verify(mock_repository).get_by_email(input_email)
        verify(mock_repository).update(expect_user)
        verify(mock_email_sender).send_password_reset_email(to_email=expect_user.email, verification_token=ANY(str))
        
    def test_email_not_found(
        self,
        request_password_reset_use_case: RequestPasswordResetUseCase,
        mock_repository: UserRepository,
        mock_email_sender: EmailSender,
        input_email: str,
    ):
        when(mock_repository).get_by_email(input_email).thenReturn(None) 
        
        response = request_password_reset_use_case.execute(input_email)
        
        assert response is None
        
        verify(mock_repository).get_by_email(input_email)
        verify(mock_repository, times=0).update(ANY(User))
        verify(mock_email_sender, times=0).send_password_reset_email(to_email=ANY(str), verification_token=ANY(str))
         
         