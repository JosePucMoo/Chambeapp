from typing import Generic, TypeVar, List
import math

from infrastructure.schemas.base_schema import BaseSchema

T = TypeVar('T')

class PaginatedResponseDTO(BaseSchema, Generic[T]):
    data: List[T]
    total_count: int
    page: int
    page_size: int
    pages: int

    @classmethod
    def create(cls, data: List[T], total_count: int, page: int, page_size: int):
        pages = math.ceil(total_count / page_size) if total_count > 0 else 0
        return cls(
            data=data, 
            total_count=total_count, 
            page=page, 
            page_size=page_size, 
            pages=pages
        )