from dataclasses import dataclass, field
import uuid


@dataclass
class User:
    name: str
    email: str
    password: str

    id: uuid.UUID = field(default_factory=uuid.uuid4)
    is_verified: bool = False
    token: str = None

    def update_profile(self, new_name: str) -> None:
        if not new_name or len(new_name.strip()) < 2:
            raise ValueError("El nombre debe tener al menos 2 caracteres")

        self.name = new_name.strip()

    def change_password(self, new_password: str) -> None:
        if not new_password:
            raise ValueError("El hash de la contraseña no puede estar vacío")

        self.password = new_password

    def mark_as_verified(self) -> None:
        self.is_verified = True

    def verify_account(self) -> None:
        self.is_verified = True
        self.token = None

    def assign_password_reset_token(self, token: str) -> None:
        self.token = token

    def clear_password_reset_token(self) -> None:
        self.token = None
