from dataclasses import dataclass, field
import uuid

@dataclass
class User:
    name: str
    email: str
    password: str

    id: uuid.UUID = field(default_factory=uuid.uuid4)
    is_verified: bool = False

@dataclass
class UpdateProfileUser:
    id: str
    name: str = None
    