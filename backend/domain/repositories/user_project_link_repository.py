from abc import ABC, abstractmethod

from domain.entities.user_project_link import UserProjectLink


class UserProjectLinkRepository(ABC):
    @abstractmethod
    def create(self, user_project_link: UserProjectLink) -> UserProjectLink:
        pass
