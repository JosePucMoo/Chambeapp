
from infrastructure.schemas.base_schema import BaseSchema


class CreateColumnDTO(BaseSchema):
    title: str
    position: int

class ColumnResponseDTO(BaseSchema):
    id: str
    title: str
    position: int
    project_id: str