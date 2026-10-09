from abc import ABC, abstractmethod
from typing import Any, Dict


class TokenGenerator(ABC):
    @abstractmethod
    def generate_token(self, data: dict) -> str:
        pass

    def decode_token(self, token: str) -> Dict[str, Any]:
        pass
