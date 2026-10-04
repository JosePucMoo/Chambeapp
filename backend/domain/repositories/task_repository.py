from abc import ABC, abstractmethod

from domain.entities.task import Task


class TaskRepository(ABC):

    @abstractmethod
    def create(self, task: Task)-> Task:
        pass

    @abstractmethod
    def get_by_id(self, task_id: str) -> Task:
        pass

    @abstractmethod
    def change_column(self, task_id: str, column_id: str) -> Task:
        pass