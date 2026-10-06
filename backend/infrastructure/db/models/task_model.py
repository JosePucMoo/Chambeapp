from datetime import datetime
from typing import Optional
import uuid

from infrastructure.db.models.base_model import Base
from domain.entities.enums import TaskPriorityEnum
from sqlalchemy import Date, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

class TaskModel(Base):
    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(String, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    priority: Mapped[TaskPriorityEnum] = mapped_column(String, nullable=False)
    due_date: Mapped[datetime] = mapped_column(Date, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, index=True)

    column_id: Mapped[str] = mapped_column(String, ForeignKey("columns.id"), nullable=False)
    assignee_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), nullable=False)

    column: Mapped["ColumnModel"] = relationship(back_populates="tasks")
    assignee: Mapped["UserModel"] = relationship(back_populates="tasks")
