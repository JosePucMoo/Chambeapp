
from abc import ABC, abstractmethod
from typing import List

from domain.entities.column import Column


class ColumnRepository(ABC):

    @abstractmethod
    def create_default_columns(self, columns: List[Column]) -> List[Column]:
        pass

    @abstractmethod
    def get_the_first_column_by_project(self, project_id: str) -> Column:
        pass

    @abstractmethod
    def get_by_id(self, column_id: str) -> Column:
        pass