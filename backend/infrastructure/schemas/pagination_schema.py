from typing import Generic, TypeVar, List
from pydantic import BaseModel
import math

T = TypeVar('T')

class PaginatedResponseDTO(BaseModel, Generic[T]):
    data: List[T]
    total_count: int
    page: int
    size: int
    pages: int

    @classmethod
    def create(cls, data: List[T], total_count: int, page: int, size: int):
        pages = math.ceil(total_count / size) if total_count > 0 else 0
        return cls(data=data, total_count=total_count, page=page, size=size, pages=pages)