import secrets
from domain.repositories.user_repository import UserRepository
from application.interfaces.email_sender import EmailSender

class RequestPasswordResetUseCase:
    def __init__(self, repository: UserRepository, email_sender: EmailSender):
        self.repository = repository
        self.email_sender = email_sender

    def execute(self, email: str) -> None:
        user = self.repository.get_by_email(email.lower())
        
        if not user:
            return

        reset_token = secrets.token_urlsafe(32)
        
        user.assign_password_reset_token(reset_token)
        self.repository.update(user)
        
        self.email_sender.send_password_reset_email(
            to_email=user.email, 
            token=reset_token
        )