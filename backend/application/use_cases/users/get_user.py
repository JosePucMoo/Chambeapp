from typing import List

from domain.exceptions.not_found_exception import NotFoundException
from domain.entities.user import User
from domain.repositories.user_repository import UserRepository

class GetUserUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute_all(self, page: int, page_size: int) -> tuple[List[User], int]:
        return self.repository.get_all(page, page_size)

    def execute_by_id(self, id: str):
        user = self.repository.get_by_id(id)
        if not user:
            raise NotFoundException('Usuario no encontrado')

        return user
        
       
