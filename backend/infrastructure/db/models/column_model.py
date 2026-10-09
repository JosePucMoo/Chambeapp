from typing import List
import uuid

from sqlalchemy import ForeignKey, Integer, String

from infrastructure.db.models.base_model import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship


class ColumnModel(Base):
    __tablename__ = "columns"

    id: Mapped[uuid.UUID] = mapped_column(String, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False)

    project_id: Mapped[str] = mapped_column(String, ForeignKey("projects.id"), nullable=False)

    project: Mapped["ProjectModel"] = relationship(back_populates="columns")
    tasks: Mapped[List["TaskModel"]] = relationship(back_populates="column")
