from dataclasses import dataclass

@dataclass
class Column:
    id: str
    title: str
    position: int
    project_id: str