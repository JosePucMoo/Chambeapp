from dataclasses import dataclasses
from datetime import datetime

@dataclasses
class Project:
    id: str
    title: str
    description: str
    client: str
    delivery_date: datetime
    created_at: datetime