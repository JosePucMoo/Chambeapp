from asyncio import Task

from sqlalchemy.orm import Session
from sqlalchemy import select

from infrastructure.db.models.task_model import TaskModel
from infrastructure.mappers.task_mappers import map_task_entity_to_model, map_task_model_to_entity
from domain.repositories.task_repository import TaskRepository

class TaskRepositoryImpl(TaskRepository):
    def __init__(self, db: Session):
        self.db = db


    def create(self, task: Task) -> Task:
        task_model = map_task_entity_to_model(task)

        self.db.add(task_model)
        self.db.commit()
        self.db.refresh(task_model)

        return map_task_model_to_entity(task_model)

    def get_by_id(self, task_id) -> Task:
        task_model = self.db.scalar(
            select(TaskModel).where(TaskModel.id == task_id)
        )

        return map_task_model_to_entity(task_model) if task_model else None

    def change_column(self, task_id: str, column_id: str) -> Task:
        task_model = self.db.scalar(
            select(TaskModel).where(TaskModel.id == task_id)
        )

        task_model.column_id = column_id

        self.db.commit()
        self.db.refresh(task_model)

        return map_task_model_to_entity(task_model)