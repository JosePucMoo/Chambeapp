from abc import ABC, abstractmethod

from domain.entities.user_project_link import UserProjectLink


class UserProjectLinkRepository(ABC):
    @abstractmethod
    def create(self, user_project_link: UserProjectLink) -> UserProjectLink:
        pass

    @abstractmethod
    def get_by_user_and_project(self, user_id: str, project_id: str) -> UserProjectLink:
        pass
