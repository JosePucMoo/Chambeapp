from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid

from domain.entities.enums import InvitationStatusEnum


@dataclass
class ProjectInvitation:
    invitee_email: str
    status: InvitationStatusEnum
    project_id: str
    invited_by: str

    token: Optional[str] = None
    expires_at: Optional[datetime] = None

    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class InvitationPreview:
    owner_name: str
    project_title: str
    invitee_email: str
    status: InvitationStatusEnum
    expires_at: datetime
