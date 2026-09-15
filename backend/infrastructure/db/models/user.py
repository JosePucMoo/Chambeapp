
from typing import List
import uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean
from infrastructure.db.models.base import Base

class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(String, primary_key=True, unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, nullable=False)

    user_board_links: Mapped[List['UserBoardLinkModel']] = relationship(back_populates='user')
    tasks: Mapped[List["TaskModel"]] = relationship(back_populates="assignee")