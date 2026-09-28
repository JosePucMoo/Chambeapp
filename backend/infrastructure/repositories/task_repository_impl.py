from asyncio import Task

from sqlalchemy.orm import Session

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