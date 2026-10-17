import jwt
import pytest

from infrastructure.security.jwt_token_generator import JwtTokenGenerator


@pytest.fixture(autouse=True)
def jwt_env(monkeypatch):
    monkeypatch.setenv("SECRET_KEY", "test-secret-key-that-is-long-enough-1234567890")
    monkeypatch.setenv("ALGORITHM", "HS256")
    monkeypatch.setenv("TOKEN_EXPIRE_MINUTES", "60")


class TestJwtTokenGenerator:
    def test_generate_and_decode_round_trip(self):
        generator = JwtTokenGenerator()

        token = generator.generate_token({"id": "user-1"})

        assert isinstance(token, str)
        payload = generator.decode_token(token)
        assert payload["id"] == "user-1"
        assert "exp" in payload

    def test_generate_token_does_not_mutate_input(self):
        generator = JwtTokenGenerator()
        data = {"id": "user-1"}

        generator.generate_token(data)

        assert data == {"id": "user-1"}

    def test_decode_with_wrong_secret_raises(self, monkeypatch):
        token = JwtTokenGenerator().generate_token({"id": "user-1"})

        monkeypatch.setenv("SECRET_KEY", "another-secret-that-is-long-enough-1234567890")
        other_generator = JwtTokenGenerator()

        with pytest.raises(jwt.InvalidTokenError):
            other_generator.decode_token(token)

    def test_expired_token_raises(self, monkeypatch):
        monkeypatch.setenv("TOKEN_EXPIRE_MINUTES", "-1")
        generator = JwtTokenGenerator()

        token = generator.generate_token({"id": "user-1"})

        with pytest.raises(jwt.ExpiredSignatureError):
            generator.decode_token(token)

    def test_missing_secret_key_raises(self, monkeypatch):
        monkeypatch.delenv("SECRET_KEY", raising=False)

        with pytest.raises(ValueError, match="SECRET_KEY environment variable is required"):
            JwtTokenGenerator()

    def test_uses_configured_algorithm(self, monkeypatch):
        monkeypatch.setenv("ALGORITHM", "HS256")
        generator = JwtTokenGenerator()

        token = generator.generate_token({"id": "user-1"})
        header = jwt.get_unverified_header(token)

        assert header["alg"] == "HS256"

    def test_expire_minutes_default(self, monkeypatch):
        monkeypatch.delenv("TOKEN_EXPIRE_MINUTES", raising=False)
        generator = JwtTokenGenerator()

        assert generator.expire_minutes == 1440

    def test_secret_key_read_from_env(self):
        generator = JwtTokenGenerator()

        assert generator.secret_key == "test-secret-key-that-is-long-enough-1234567890"
