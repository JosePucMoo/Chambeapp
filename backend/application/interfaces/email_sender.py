from abc import ABC, abstractmethod


class EmailSender(ABC):
    @abstractmethod
    def send_verification_email(self, to_email: str, verification_token: str) -> None:
        pass

    @abstractmethod
    def send_password_reset_email(self, to_email: str, verification_token: str) -> None:
        pass
