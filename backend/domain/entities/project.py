from dataclasses import dataclass, field
from datetime import date, datetime
import math
from typing import List
import uuid

from sqlalchemy import Column

from domain.entities.enums import ProjectStatusEnum, RoleEnum

@dataclass
class Project:
    title: str
    description: str
    client: str
    delivery_date: datetime

    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class ProjectDashboardSummary:
    id: int
    title: str
    client: str
    role: RoleEnum
    delivery_date: date
    total_tasks: int
    completed_tasks: int
    not_started_tasks: int
    
    progress_percentage: float = field(init=False)
    status: ProjectStatusEnum = field(init=False)

    def __post_init__(self):

        if self.total_tasks > 0:
            progress = (self.completed_tasks / self.total_tasks) * 100.0
            self.progress_percentage = math.ceil(progress)
        else:
            self.progress_percentage = 0.0

        today = date.today()

        if self.delivery_date < today and (self.completed_tasks != self.total_tasks) :
            self.status = ProjectStatusEnum.DELAYED
    
        elif self.total_tasks == 0:
            self.status = ProjectStatusEnum.NOT_STARTED
            
        elif self.completed_tasks == self.total_tasks: 
            self.status = ProjectStatusEnum.COMPLETED
            
        elif self.not_started_tasks == self.total_tasks:
            self.status = ProjectStatusEnum.NOT_STARTED
            
        else:
            self.status = ProjectStatusEnum.ACTIVE

@dataclass
class ProjectMember:
    id: str
    name: str
    email: str

@dataclass
class ProjectBoard:
    project_id: str
    project_title: str
    columns: List[Column]