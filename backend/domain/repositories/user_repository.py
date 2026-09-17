from abc import ABC, abstractmethod
from typing import List

from domain.entities.user import User

class UserRepository(ABC):

    @abstractmethod
    def create(self, user: User) -> User:
        pass

    @abstractmethod
    def get_all(self, page: int, page_size: int) -> List[User]:
        pass

    @abstractmethod
    def get_by_id(self, id: str) -> User | None:
        pass