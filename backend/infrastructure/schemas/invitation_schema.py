from datetime import datetime

from pydantic import EmailStr

from domain.entities.enums import InvitationStatusEnum
from infrastructure.schemas.base_schema import BaseSchema


class InviteMemberDTO(BaseSchema):
    email: EmailStr


class InvitePreviewDTO(BaseSchema):
    owner_name: str
    project_title: str
    invitee_email: str
    status: InvitationStatusEnum
    expires_at: datetime


class AcceptInvitationDTO(BaseSchema):
    project_id: str
