
from typing import List
from datetime import datetime
import uuid

from sqlalchemy import Date, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.db.models.base_model import Base

class BoardModel(Base):
    __tablename__= 'boards'

    id: Mapped[uuid.UUID] = mapped_column(String, primary_key=True, unique=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False, index=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    client: Mapped[str] = mapped_column(String, nullable=False)
    delivery_date: Mapped[datetime] = mapped_column(Date, nullable=False)
    created_at: Mapped[datetime] = mapped_column(Date, default=datetime.utcnow)

    user_board_links: Mapped[List["UserBoardLinkModel"]] = relationship(back_populates="board")
    columns: Mapped["ColumnModel"] = relationship(back_populates="board")