from abc import ABC, abstractmethod
from typing import List, Optional

from domain.entities.user import User


class UserRepository(ABC):
    @abstractmethod
    def create(self, user: User) -> User:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def get_all(self, page: int, page_size: int) -> List[User]:
        pass

    @abstractmethod
    def get_by_id(self, id: str) -> Optional[User]:
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        pass

    @abstractmethod
    def get_by_token(self, token: str) -> Optional[User]:
        pass
