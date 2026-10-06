from typing import Optional

from domain.entities.task import TaskFilters
from infrastructure.db.models.column_model import ColumnModel
from infrastructure.db.models.project_model import ProjectModel
from infrastructure.db.models.task_model import TaskModel


def apply_task_filters(conditions: list, filters: Optional[TaskFilters] = None) -> None:
    if not filters:
        return

    if filters.priority:
        conditions.append(TaskModel.priority == filters.priority)

    if filters.column_title:
        conditions.append(ColumnModel.title == filters.column_title)

    if filters.project_id:
        conditions.append(ProjectModel.id == filters.project_id)

    if filters.search:
        conditions.append(TaskModel.title.ilike(f"%{filters.search.strip()}%"))

    if filters.start_date:
        conditions.append(TaskModel.due_date >= filters.start_date)

    if filters.end_date:
        conditions.append(TaskModel.due_date <= filters.end_date)
