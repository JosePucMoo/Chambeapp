from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from domain.entities.enums import InvitationStatusEnum
from infrastructure.db.models.base_model import Base


class ProjectInvitationModel(Base):
    __tablename__ = "project_invitations"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    token: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False )
    invitee_email: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[InvitationStatusEnum] = mapped_column(String(100), default=InvitationStatusEnum.PENDING, nullable=False)

    project_id: Mapped[str] = mapped_column(String, ForeignKey("projects.id"), nullable=False)
    invited_by: Mapped[str] = mapped_column(String, ForeignKey("users.id"), nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default= datetime.utcnow(), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)