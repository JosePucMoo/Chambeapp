import os

import jwt
from datetime import datetime, timedelta, timezone
from application.interfaces.token_generator import TokenGenerator

class JwtTokenGenerator(TokenGenerator):
    def __init__(self):
        self.secret_key = os.getenv("SECRET_KEY", "change-me-in-prod")
        self.algorithm = os.getenv("ALGORITHM", "HS256")
        self.expire_minutes = int(os.getenv("TOKEN_EXPIRE_MINUTES", "1440"))

    def generate_token(self, data: dict) -> str:
        to_encode = data.copy()
        
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.expire_minutes)
        
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def decode_token(self, token: str) -> dict:
        payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        return payload