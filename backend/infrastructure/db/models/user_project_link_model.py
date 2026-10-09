import uuid

from sqlalchemy import ForeignKey, String

from infrastructure.db.models.base_model import Base
from domain.entities.enums import RoleEnum

from sqlalchemy.orm import Mapped, mapped_column, relationship


class UserProjectLinkModel(Base):
    __tablename__ = "user_project_link"

    id: Mapped[uuid.UUID] = mapped_column(String, unique=True, primary_key=True, index=True)
    role: Mapped[RoleEnum] = mapped_column(String, nullable=False)

    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), nullable=False)
    project_id: Mapped[str] = mapped_column(String, ForeignKey("projects.id"), nullable=False)

    user: Mapped["UserModel"] = relationship(back_populates="user_project_links")
    project: Mapped["ProjectModel"] = relationship(back_populates="user_project_links")
