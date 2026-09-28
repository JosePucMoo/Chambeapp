from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid

@dataclass
class Task:
    title: str
    description: str
    priority: str
    due_date: datetime
    column_id: str
    assignee_id: str

    id: uuid.UUID = field(default_factory=uuid.uuid4)