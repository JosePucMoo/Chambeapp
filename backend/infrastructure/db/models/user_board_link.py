from datetime import datetime
import uuid

from sqlalchemy import Date, ForeignKey, String

from infrastructure.db.models.base import Base
from domain.entities.enums import RoleEnum

from sqlalchemy.orm import Mapped, mapped_column, relationship

class UserBoardLinkModel(Base):
    __tablename__= 'user_board_link'

    id: Mapped[uuid.UUID] = mapped_column(String, unique=True, primary_key=True, index=True)
    role: Mapped[RoleEnum] = mapped_column(String, nullable=False)
    joined_at: Mapped[datetime] = mapped_column(Date, nullable=False, default=datetime.utcnow)

    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), nullable=False) 
    board_id: Mapped[str] = mapped_column(String, ForeignKey("boards.id"), nullable=False)

    user: Mapped["UserModel"] = relationship(back_populates='user_board_links')
    board: Mapped["BoardModel"] = relationship(back_populates='user_board_links')