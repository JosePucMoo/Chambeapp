import secrets

from application.interfaces.password_hasher import PasswordHasher
from application.interfaces.email_sender import EmailSender
from domain.utils.constants import Constants
from domain.entities.user import User
from domain.repositories.user_repository import UserRepository
from domain.exceptions.cannot_create_exception import CannotCreateException
from domain.exceptions.resource_alredy_exists_exception import ResourceAlreadyExistsException


class RegisterUserUseCase:
    def __init__(
        self, repository: UserRepository, password_hasher: PasswordHasher, email_sender: EmailSender
    ):
        self.repository = repository
        self.password_hasher = password_hasher
        self.email_sender = email_sender

    def execute(self, user_data: User) -> User:
        if self.repository.get_by_email(user_data.email):
            raise ResourceAlreadyExistsException(Constants.EMAIL_ALREADY_EXISTS)

        password_hashed = self.password_hasher.hash(user_data.password)
        verification_token = secrets.token_urlsafe(32)

        user = User(
            name=user_data.name,
            email=user_data.email,
            password=password_hashed,
            token=verification_token,
        )
        saved_user = self.repository.create(user)

        if not saved_user:
            raise CannotCreateException(Constants.USER_NOT_CREATED)

        self.email_sender.send_verification_email(
            to_email=saved_user.email, verification_token=verification_token
        )

        return saved_user
