from dataclasses import dataclass, field
from datetime import datetime
import uuid

@dataclass
class Taks:
    title: str
    description: str
    priority: str
    due_date: datetime
    column_id: str
    assignee_id: str
    created_at: datetime

    id: uuid.UUID = field(default_factory=uuid.uuid4)