import jwt
from datetime import datetime, timedelta, timezone
from application.interfaces.token_generator import TokenGenerator

class JwtTokenGenerator(TokenGenerator):
    def __init__(self, secret_key: str, algorithm: str = "HS256", expire_minutes: int = 1440):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expire_minutes = expire_minutes

    def generate_token(self, data: dict) -> str:
        to_encode = data.copy()
        
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.expire_minutes)
        
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt