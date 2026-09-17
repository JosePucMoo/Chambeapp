from abc import ABC, abstractmethod

from domain.entities.user import User

class UserRepository(ABC):

    @abstractmethod
    def create(self, user: User) -> User:
        pass