from infrastructure.security.password_hasher_impl import PasswordHasherImpl


class TestPasswordHasherImpl:
    def setup_method(self):
        self.hasher = PasswordHasherImpl()

    def test_hash_returns_a_string_different_from_plain(self):
        hashed = self.hasher.hash("password123")

        assert isinstance(hashed, str)
        assert hashed != "password123"

    def test_hash_is_salted(self):
        first = self.hasher.hash("password123")
        second = self.hasher.hash("password123")

        assert first != second

    def test_verify_returns_true_for_correct_password(self):
        hashed = self.hasher.hash("password123")

        assert self.hasher.verify("password123", hashed) is True

    def test_verify_returns_false_for_wrong_password(self):
        hashed = self.hasher.hash("password123")

        assert self.hasher.verify("wrong-password", hashed) is False
