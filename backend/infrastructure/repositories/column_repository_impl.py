from typing import List

from psycopg import Column
from sqlalchemy import select
from sqlalchemy.orm import Session

from infrastructure.db.models.column_model import ColumnModel
from domain.repositories.column_repository import ColumnRepository
from infrastructure.mappers.column_mappers import (
    map_column_entity_to_model,
    map_column_model_to_entity,
)


class ColumnRepositoryImpl(ColumnRepository):
    def __init__(self, db: Session):
        self.db = db

    def create_default_columns(self, columns: List[Column]) -> List[Column]:
        columns_model = [map_column_entity_to_model(column) for column in columns]

        self.db.add_all(columns_model)

        self.db.commit()

        for model in columns_model:
            self.db.refresh(model)

        return [map_column_model_to_entity(model) for model in columns_model]

    def get_the_first_column_by_project(self, project_id: str) -> Column:
        query = (
            select(ColumnModel)
            .filter(ColumnModel.project_id == project_id)
            .order_by(ColumnModel.position.asc())
        )

        column_model = self.db.scalar(query)

        return map_column_model_to_entity(column_model) if column_model else None

    def get_by_id(self, column_id: str) -> Column:
        column_model = self.db.scalar(select(ColumnModel).where(ColumnModel.id == column_id))

        return map_column_model_to_entity(column_model) if column_model else None
