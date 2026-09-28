
from abc import ABC, abstractmethod
from typing import List

from domain.entities.column import Column


class ColumnRepository(ABC):

    @abstractmethod
    def create_default_columns(self, columns: List[Column]) -> List[Column]:
        pass