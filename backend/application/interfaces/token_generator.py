from abc import ABC, abstractmethod

class TokenGenerator(ABC):
    @abstractmethod
    def generate_token(self, data: dict) -> str:
        pass