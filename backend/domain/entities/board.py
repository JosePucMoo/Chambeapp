from dataclasses import dataclasses
from datetime import datetime

class Board:
    id: str
    title: str
    description: str
    client: str
    delivery_date: datetime
    created_at: datetime