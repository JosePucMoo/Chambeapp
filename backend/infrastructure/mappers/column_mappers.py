from domain.entities.column import Column
from infrastructure.db.models.column_model import ColumnModel
from infrastructure.schemas.column_schema import ColumnResponseDTO


def map_column_entity_to_dto(column: Column) -> ColumnResponseDTO:
    return ColumnResponseDTO(
        id=column.id, title=column.title, position=column.position, project_id=column.project_id
    )


def map_column_model_to_entity(column: ColumnModel) -> Column:
    return Column(
        id=column.id, title=column.title, position=column.position, project_id=column.project_id
    )


def map_column_entity_to_model(column: Column) -> ColumnModel:
    return ColumnModel(
        id=column.id, title=column.title, position=column.position, project_id=column.project_id
    )
