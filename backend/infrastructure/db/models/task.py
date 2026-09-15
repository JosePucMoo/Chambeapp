from datetime import datetime
import uuid

from infrastructure.db.models.base import Base
from domain.entities.enums import PriorityLevelEnum
from sqlalchemy import Date, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

class TaskModel(Base):
    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(String, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    priority: Mapped[PriorityLevelEnum] = mapped_column(String, nullable=False, default=PriorityLevelEnum.low)
    due_date: Mapped[datetime] = mapped_column(Date, nullable=False)

    column_id: Mapped[str] = mapped_column(String, ForeignKey("columns.id"), nullable=False)
    assignee_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), nullable=False)

    column: Mapped["ColumnModel"] = relationship(back_populates="tasks")
    assignee: Mapped["UserModel"] = relationship(back_populates="tasks")
