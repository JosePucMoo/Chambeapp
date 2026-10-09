from dataclasses import dataclass, field
import uuid


@dataclass
class UserProjectLink:
    role: str
    user_id: str
    project_id: str

    id: uuid.UUID = field(default_factory=uuid.uuid4)
