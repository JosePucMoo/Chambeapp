from abc import ABC, abstractmethod

from domain.entities.project import Project


class ProjectRepository(ABC):

    @abstractmethod
    def create(self, project: Project) -> Project:
        pass