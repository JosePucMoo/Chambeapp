from typing import List

from domain.entities.user import User
from domain.repositories.user_repository import UserRepository

class GetUserUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute_all(self, page: int, page_size: int) -> tuple[List[User], int]:
        return self.repository.get_all(page, page_size)
       
