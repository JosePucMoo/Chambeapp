
from domain.entities.user import User
from infrastructure.repositories.user_repository_impl import UserRepositoryImpl

class TestUserRepository:
        
    def test_create_successfully(self, db_session):
        repository = UserRepositoryImpl(db_session)
        user = User(name="Test", email="test@test.com", password="hashed")
        created_user = repository.create(user)
        assert created_user.id is not None
        
        assert created_user is not None
        assert created_user.email == "test@test.com"
        
    def test_get_by_email_succesfully(self, db_session):
        repository = UserRepositoryImpl(db_session)
        user = User(name="Test", email="test@test.com", password="hashed")
        created_user = repository.create(user)
        
        user_db = repository.get_by_email(created_user.email)
        assert user_db is not None
        assert user_db.email == "test@test.com"
        
    def test_not_found_by_email(self, db_session):
        repository = UserRepositoryImpl(db_session)        
        user_db = repository.get_by_email("test@test.com")
        
        assert user_db is None
    
    def test_get_by_token_sucessfully(self, db_session):
        repository = UserRepositoryImpl(db_session)
        user = User(name="Test", email="test@test.com", password="hashed", token="token-secret")
        created_user = repository.create(user)
        
        user_db = repository.get_by_token(created_user.token)
        assert user_db is not None
        assert user_db.email == "test@test.com"
        
    def test_not_found_by_token(self, db_session):
        repository = UserRepositoryImpl(db_session)        
        user_db = repository.get_by_token("token-secret")
        
        assert user_db is None
        
    def test_update_successfully(self, db_session):
        repository = UserRepositoryImpl(db_session)
        user = User(name="Test", email="test@test.com", password="hashed")
        created_user = repository.create(user)
        assert created_user.id is not None
        
        created_user.name = 'NewTest'
        created_user.email = 'newemail@test.com'
        
        updated_user = repository.update(created_user)
        
        assert updated_user is not None
        assert updated_user.name == "NewTest"
        assert updated_user.email == "newemail@test.com"
        
    