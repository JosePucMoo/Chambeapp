from asyncio import Task, tasks
from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import func, select

from infrastructure.db.models.column_model import ColumnModel
from infrastructure.db.models.project_model import ProjectModel
from domain.entities.task import TaskDashboardSummary
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

    def get_paginated_dashboard_tasks(self, user_id: str, page: int, page_size: int) -> tuple[int, List[TaskDashboardSummary]]:
        query_total_items = select(func.count(TaskModel.id)).where(TaskModel.assignee_id == user_id)
        
        total_items = self.db.execute(query_total_items).scalar()
        
        offset = (page - 1) * page_size

        query = select(
            TaskModel.id,
            TaskModel.title,
            TaskModel.due_date,
            TaskModel.priority,
            ColumnModel.title.label("column_title"),
            ProjectModel.title.label("project_title")
            ).join(
                ColumnModel, TaskModel.column_id == ColumnModel.id
            ).join(
                ProjectModel, ColumnModel.project_id == ProjectModel.id
            ).filter(
                TaskModel.assignee_id == user_id
            ).offset(offset).limit(page_size)

        results = self.db.execute(query).all() 

        tasks = [
            TaskDashboardSummary(
                id=row.id,
                title=row.title,
                priority=row.priority,
                due_date=row.due_date,
                column_title=row.column_title,
                project_title=row.project_title
            )
            for row in results
        ]

        return (total_items, tasks)