from dataclasses import dataclass, field
from datetime import datetime
import uuid

@dataclass
class Project:
    title: str
    description: str
    client: str
    delivery_date: datetime
    created_at: datetime

    id: uuid.UUID = field(default_factory=uuid.uuid4)