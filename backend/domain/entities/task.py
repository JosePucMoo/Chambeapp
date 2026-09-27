from dataclasses import dataclass
from datetime import datetime

@dataclass
class Taks:
    title: str
    description: str
    priority: str
    due_date: datetime
    column_id: str
    assignee_id: str
    created_at: datetime