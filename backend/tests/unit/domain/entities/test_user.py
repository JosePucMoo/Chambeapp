import uuid

from domain.entities.user import User


class TestUser:

    def test_user_create_with_required_fields(self):
        user = User(name="Juan Pérez", email="juan@test.com", password="hashed_password")

        assert user.name == "Juan Pérez"
        assert user.email == "juan@test.com"
        assert user.password == "hashed_password"
        assert isinstance(user.id, uuid.UUID)
        assert user.is_verified is False
        assert user.token is None


    def test_user_create_with_custom_id(self):
        custom_id = uuid.uuid4()
        user = User(
            name="Ana García",
            email="ana@test.com",
            password="hashed_password",
            id=custom_id,
            is_verified=True,
            token="reset_token_123",
        )

        assert user.id == custom_id
        assert user.is_verified is True
        assert user.token == "reset_token_123"


    def test_update_profile_success(self):
        user = User(name="Juan", email="juan@test.com", password="hashed_password")
        user.update_profile("María González")

        assert user.name == "María González"


    def test_update_profile_strips_whitespace(self):
        user = User(name="Juan", email="juan@test.com", password="hashed_password")
        user.update_profile("  Carlos López  ")

        assert user.name == "Carlos López"


    def test_update_profile_raises_error_for_empty_name(self):
        user = User(name="Juan", email="juan@test.com", password="hashed_password")

        try:
            user.update_profile("")
            assert False, "Expected ValueError"
        except ValueError as e:
            assert str(e) == "El nombre debe tener al menos 2 caracteres"


    def test_update_profile_raises_error_for_short_name(self):
        user = User(name="Juan", email="juan@test.com", password="hashed_password")

        try:
            user.update_profile("A")
            assert False, "Expected ValueError"
        except ValueError as e:
            assert str(e) == "El nombre debe tener al menos 2 caracteres"


    def test_update_profile_raises_error_for_whitespace_only_name(self):
        user = User(name="Juan", email="juan@test.com", password="hashed_password")

        try:
            user.update_profile("   ")
            assert False, "Expected ValueError"
        except ValueError as e:
            assert str(e) == "El nombre debe tener al menos 2 caracteres"


    def test_change_password_success(self):
        user = User(name="Juan", email="juan@test.com", password="old_password")
        user.change_password("new_hashed_password")

        assert user.password == "new_hashed_password"


    def test_change_password_raises_error_for_empty_password(self):
        user = User(name="Juan", email="juan@test.com", password="old_password")

        try:
            user.change_password("")
            assert False, "Expected ValueError"
        except ValueError as e:
            assert str(e) == "El hash de la contraseña no puede estar vacío"


    def test_mark_as_verified(self):
        user = User(name="Juan", email="juan@test.com", password="hashed_password")
        assert user.is_verified is False

        user.mark_as_verified()
        assert user.is_verified is True


    def test_verify_account(self):
        user = User(name="Juan", email="juan@test.com", password="hashed_password", token="some_token")
        assert user.is_verified is False
        assert user.token == "some_token"

        user.verify_account()
        assert user.is_verified is True
        assert user.token is None


    def test_assign_password_reset_token(self):
        user = User(name="Juan", email="juan@test.com", password="hashed_password")
        user.assign_password_reset_token("reset_token_abc123")

        assert user.token == "reset_token_abc123"


    def test_clear_password_reset_token(self):
        user = User(name="Juan", email="juan@test.com", password="hashed_password", token="reset_token_abc123")
        user.clear_password_reset_token()

        assert user.token is None
