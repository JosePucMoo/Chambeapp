from dataclasses import dataclass, field
from datetime import datetime
import uuid

from domain.entities.enums import InvitationStatusEnum


@dataclass
class ProjectInvitation:
    token: str
    invitee_email: str
    status: InvitationStatusEnum
    project_id: str
    invited_by: str
    expires_at: datetime

    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default_factory=datetime.utcnow)
