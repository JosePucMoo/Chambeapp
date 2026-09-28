

from datetime import datetime

from infrastructure.schemas.base_schema import BaseSchema

class CreateProjectDTO(BaseSchema):
    title: str
    description: str
    client: str
    delivery_date: datetime

class ProjectResponseDTO(BaseSchema):
    id: str
    title: str
    description: str
    client: str
    delivery_date: datetime
 