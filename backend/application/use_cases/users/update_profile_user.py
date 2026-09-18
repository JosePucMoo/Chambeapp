from domain.exceptions.cannot_update_exception import CannotUpdateException
from domain.exceptions.not_found_exception import NotFoundException
from domain.repositories.user_repository import UserRepository


class UpdateUserUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(self, user_id: str, new_name: str):
        user = self.repository.get_by_id(user_id)
        if not user:
            raise NotFoundException('Usuario no encontrado')

        user.update_profile(new_name)

        updated_user = self.repository.update(user)

        if not updated_user:
            raise CannotUpdateException('El usuario no pudo ser actualizado')

        return updated_user

        