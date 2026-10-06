from asyncio import Task, tasks
from datetime import date, datetime, timedelta
from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import and_, case, func, not_, select

from infrastructure.db.models.column_model import ColumnModel
from infrastructure.db.models.project_model import ProjectModel
from domain.entities.task import DailyTaskActivity, TaskDashboardSummary, TaskDueSoon, TaskMetricsAggregate
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

        target_column = self.db.scalar(
            select(ColumnModel).where(ColumnModel.id == column_id)
        )

        is_completed_column = self._is_completed_column(target_column)

        moved = task_model.column_id != column_id

        task_model.column_id = column_id

        if is_completed_column:
            if moved or task_model.completed_at is None:
                task_model.completed_at = datetime.utcnow()
        else:
            task_model.completed_at = None

        self.db.commit()
        self.db.refresh(task_model)

        return map_task_model_to_entity(task_model)

    def _is_completed_column(self, column_model: ColumnModel) -> bool:
        max_position = self.db.scalar(
            select(func.max(ColumnModel.position)).where(
                ColumnModel.project_id == column_model.project_id
            )
        )

        return column_model.position == max_position

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

    def get_metrics(self, user_id: str, due_from: date, due_to: date) -> TaskMetricsAggregate:
        completed_condition = TaskModel.column_id.in_(
            self._completed_column_ids_query()
        )

        due_soon_condition = and_(
            not_(completed_condition),
            TaskModel.due_date >= due_from,
            TaskModel.due_date <= due_to
        )

        query = select(
            func.count(TaskModel.id).label("total_tasks"),
            func.count(case((completed_condition, TaskModel.id))).label("completed_tasks"),
            func.count(case((due_soon_condition, TaskModel.id))).label("tasks_due_soon")
        ).where(
            TaskModel.assignee_id == user_id
        )

        row = self.db.execute(query).one()

        return TaskMetricsAggregate(
            total_tasks=row.total_tasks,
            completed_tasks=row.completed_tasks,
            tasks_due_soon=row.tasks_due_soon
        )

    def get_due_soon_tasks(self, user_id: str, due_from: date, due_to: date) -> List[TaskDueSoon]:
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
        ).where(
            TaskModel.assignee_id == user_id,
            TaskModel.column_id.notin_(self._completed_column_ids_query()),
            TaskModel.due_date >= due_from,
            TaskModel.due_date <= due_to
        ).order_by(
            TaskModel.due_date.asc(),
            TaskModel.title.asc()
        )

        results = self.db.execute(query).all()

        return [
            TaskDueSoon(
                id=row.id,
                title=row.title,
                priority=row.priority,
                due_date=row.due_date,
                column_title=row.column_title,
                project_title=row.project_title
            )
            for row in results
        ]

    def get_weekly_activity(self, user_id: str, start_at: datetime, end_at: datetime) -> List[DailyTaskActivity]:
        created_subquery = (
            select(
                func.date(TaskModel.created_at).label("day"),
                func.count(TaskModel.id).label("created")
            )
            .where(
                TaskModel.assignee_id == user_id,
                TaskModel.created_at >= start_at,
                TaskModel.created_at < end_at
            )
            .group_by(func.date(TaskModel.created_at))
            .subquery()
        )

        completed_subquery = (
            select(
                func.date(TaskModel.completed_at).label("day"),
                func.count(TaskModel.id).label("completed")
            )
            .where(
                TaskModel.assignee_id == user_id,
                TaskModel.completed_at >= start_at,
                TaskModel.completed_at < end_at
            )
            .group_by(func.date(TaskModel.completed_at))
            .subquery()
        )

        days = (
            func.generate_series(start_at, end_at - timedelta(days=1), timedelta(days=1))
            .table_valued("day")
            .render_derived(name="series_days")
        )

        query = (
            select(
                days.c.day.label("day"),
                func.coalesce(created_subquery.c.created, 0).label("created"),
                func.coalesce(completed_subquery.c.completed, 0).label("completed")
            )
            .select_from(days)
            .outerjoin(created_subquery, created_subquery.c.day == days.c.day)
            .outerjoin(completed_subquery, completed_subquery.c.day == days.c.day)
            .order_by(days.c.day)
        )

        results = self.db.execute(query).all()

        return [
            DailyTaskActivity(
                day=row.day.date() if isinstance(row.day, datetime) else row.day,
                created=row.created,
                completed=row.completed
            )
            for row in results
        ]

    def _completed_column_ids_query(self):
        column_positions = (
            select(
                ColumnModel.project_id,
                func.max(ColumnModel.position).label("max_position")
            )
            .group_by(ColumnModel.project_id)
            .subquery()
        )

        return select(ColumnModel.id).join(
            column_positions, ColumnModel.project_id == column_positions.c.project_id
        ).where(
            ColumnModel.position == column_positions.c.max_position
        )