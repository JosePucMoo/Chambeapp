from dataclasses import dataclass

@dataclass
class Column:
    id: str
    title: str
    position: int
    board_id: str