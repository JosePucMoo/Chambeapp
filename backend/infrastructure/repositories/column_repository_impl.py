
from typing import List

from psycopg import Column
from sqlalchemy.orm import Session

from domain.repositories.column_repository import ColumnRepository
from infrastructure.mappers.column_mappers import map_column_entity_to_model, map_column_model_to_entity

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