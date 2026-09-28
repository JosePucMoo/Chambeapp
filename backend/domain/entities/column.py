from dataclasses import dataclass, field
import uuid

@dataclass
class Column:
    title: str
    position: int
    project_id: str

    id: uuid.UUID = field(default_factory=uuid.uuid4)