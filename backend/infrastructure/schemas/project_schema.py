

from datetime import datetime

from pydantic import ConfigDict

from domain.entities.enums import RoleEnum
from infrastructure.schemas.base_schema import BaseSchema

class BaseProjectDTO(BaseSchema):
    title: str
    description: str
    client: str
    delivery_date: datetime

class CreateProjectDTO(BaseProjectDTO):

    model_config = ConfigDict(from_attributes=True)

class ProjectResponseDTO(BaseProjectDTO):
    id: str

    model_config = ConfigDict(from_attributes=True)

class ProjectDashboardSummaryDTO(BaseSchema):
    id: str
    title: str
    client: str
    role: str
    delivery_date: datetime
    status: str
    progress_percentage: float

class ProjectMemberResponseDTO(BaseSchema):
    id: str
    name: str
    email: str