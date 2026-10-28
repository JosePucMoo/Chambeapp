import bcrypt

from application.interfaces.password_hasher import PasswordHasher


class PasswordHasherImpl(PasswordHasher):
    def hash(self, password: str) -> str:
        pwd_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        hashed_bytes = bcrypt.hashpw(pwd_bytes, salt)

        return hashed_bytes.decode("utf-8")

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        plain_bytes = plain_password.encode("utf-8")
        hashed_bytes = hashed_password.encode("utf-8")

        return bcrypt.checkpw(plain_bytes, hashed_bytes)
