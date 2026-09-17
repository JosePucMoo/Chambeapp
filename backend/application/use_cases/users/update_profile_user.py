from domain.exceptions.resource_alredy_exists_exception import ResourceAlreadyExistsException
from domain.exceptions.cannot_update_exception import CannotUpdateException
from domain.entities.user import UpdateProfileUser, User
from domain.exceptions.not_found_exception import NotFoundException
from domain.repositories.user_repository import UserRepository


class UpdateUserUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(self, user_data: UpdateProfileUser):
        if not self.repository.get_by_id(user_data.id):
            raise NotFoundException('Usuario no encontrado')

        updated_user = self.repository.update(user_data)

        if not updated_user:
            raise CannotUpdateException('El usuario no pudo ser actualizado')

        return updated_user

        