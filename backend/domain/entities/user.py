from dataclasses import dataclass, field
from typing import Optional
import uuid

@dataclass
class User:
    name: str
    email: str
    password: str

    id: uuid.UUID = field(default_factory=uuid.uuid4)
    is_verified: bool = False

    def update_profile(self, new_name: str) -> None:
        if not new_name or len(new_name.strip()) < 2:
            raise ValueError("El nombre debe tener al menos 2 caracteres")
        
        self.name = new_name.strip()

    def change_password(self, new_hashed_password: str) -> None:
        if not new_hashed_password:
            raise ValueError("El hash de la contraseña no puede estar vacío")
        
        self.hashed_password = new_hashed_password

    def mark_as_verified(self) -> None:
        self.is_verified = True
