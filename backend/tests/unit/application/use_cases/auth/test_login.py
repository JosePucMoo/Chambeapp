
from mockito import verify, when

import pytest

from application.interfaces.password_hasher import PasswordHasher
from application.interfaces.token_generator import TokenGenerator
from application.use_cases.auth.login import LoginUseCase
from domain.exceptions.unverified_account_exception import UnverifiedAccountException
from domain.exceptions.invalid_credentials_exception import InvalidCredentialsException
from domain.utils.constants import Constants
from domain.entities.user import User
from domain.repositories.user_repository import UserRepository


class TestLoginUseCase:
    
    @pytest.fixture
    def fake_user(self) -> User:
        user = User(
            name="test",
            email="test@email.com",
            password="hashed_password",
            is_verified=True,
            token="jwt.fake.token"
        )
        return user
    
    def test_login_succesfully(
        self,
        login_use_case: LoginUseCase,
        mock_repository: UserRepository,
        mock_password_hasher: PasswordHasher,
        mock_token_generator: TokenGenerator,
        fake_user: User
    ):
                
        payload = {
            'id': str(fake_user.id)
        }
        when(mock_repository).get_by_email(fake_user.email).thenReturn(fake_user)     
        when(mock_password_hasher).verify(fake_user.password, fake_user.password).thenReturn(True)
        when(mock_token_generator).generate_token(payload).thenReturn(fake_user.token)   
        
        token, user = login_use_case.execute(
            email=fake_user.email, 
            password=fake_user.password
        )
        
        assert token == fake_user.token
        assert user == fake_user
        
        verify(mock_repository, times=1).get_by_email(fake_user.email)        
        verify(mock_password_hasher, times=1).verify(fake_user.password, fake_user.password)        
        verify(mock_token_generator, times=1).generate_token(payload)
        
        
    def test_login_not_user_found(
            self,
            login_use_case,
            mock_repository: UserRepository,
            fake_user: User
        ):
            
            when(mock_repository).get_by_email(fake_user.email).thenReturn(None)

            
            with pytest.raises(InvalidCredentialsException, match=Constants.INVALID_CREDENTIALS):
                token, user = login_use_case.execute(
                    email=fake_user.email, 
                    password=fake_user.password
                )
            
            verify(mock_repository, times=1).get_by_email(fake_user.email)  
            
    def test_login_wrong_password(
            self,
            login_use_case,
            mock_repository: UserRepository,
            mock_password_hasher: PasswordHasher,
            fake_user: User
        ):

            when(mock_repository).get_by_email(fake_user.email).thenReturn(fake_user)
            when(mock_password_hasher).verify(fake_user.password, fake_user.password).thenReturn(False)

            with pytest.raises(InvalidCredentialsException, match=Constants.INVALID_CREDENTIALS):
                token, user = login_use_case.execute(
                    email=fake_user.email, 
                    password=fake_user.password
                )

            verify(mock_repository, times=1).get_by_email(fake_user.email)  
            verify(mock_password_hasher, times=1).verify(fake_user.password, fake_user.password)  
                  
    def test_login_user_not_verified(
        self,
        login_use_case,
        mock_repository: UserRepository,
        mock_password_hasher: PasswordHasher,
        fake_user: User
    ):
        fake_user.is_verified = False

        when(mock_repository).get_by_email(fake_user.email).thenReturn(fake_user)
        when(mock_password_hasher).verify(fake_user.password, fake_user.password).thenReturn(True)

        with pytest.raises(UnverifiedAccountException, match=Constants.UNVERIFIED_ACCOUNT):
            token, user = login_use_case.execute(
                email=fake_user.email, 
                password=fake_user.password
            )

        verify(mock_repository, times=1).get_by_email(fake_user.email)  
        verify(mock_password_hasher, times=1).verify(fake_user.password, fake_user.password) 