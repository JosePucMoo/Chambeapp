from typing import List, Optional
from datetime import date

from sqlalchemy import and_, case, func, select
from sqlalchemy.orm import joinedload

from domain.entities.column import ColumnBoard
from domain.entities.task import TaskBoard, TaskFilters
from infrastructure.db.models.user_model import UserModel
from domain.entities.enums import ProjectStatusEnum, RoleEnum, TaskPriorityEnum
from infrastructure.db.models.column_model import ColumnModel
from infrastructure.db.models.project_model import ProjectModel
from infrastructure.db.models.user_project_link_model import UserProjectLinkModel
from infrastructure.db.models.task_model import TaskModel
from infrastructure.mappers.project_mappers import (
    map_project_entity_to_model,
    map_project_model_to_entity,
)
from domain.entities.project import (
    Project,
    ProjectBoard,
    ProjectDashboardSummary,
    ProjectFilters,
    ProjectMember,
)
from domain.repositories.project_repository import ProjectRepository
from sqlalchemy.orm import Session

from infrastructure.repositories.filters import apply_task_filters


class ProjectRepositoryImpl(ProjectRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, project: Project) -> Project:
        project_model = map_project_entity_to_model(project)

        self.db.add(project_model)
        self.db.commit()
        self.db.refresh(project_model)

        return map_project_model_to_entity(project_model)

    def update(self, project: Project) -> Optional[Project]:
        project_model = self.db.query(ProjectModel).filter(ProjectModel.id == project.id).first()

        if not project_model:
            return None

        project_model.title = project.title
        project_model.description = project.description
        project_model.client = project.client
        project_model.delivery_date = project.delivery_date

        self.db.commit()
        self.db.refresh(project_model)

        return map_project_model_to_entity(project_model)

    def _summaries_query(self, user_id: str):
        subquery_positions = (
            self.db.query(
                ColumnModel.project_id,
                func.max(ColumnModel.position).label("max_pos"),
                func.min(ColumnModel.position).label("min_pos"),
            )
            .group_by(ColumnModel.project_id)
            .subquery()
        )

        return (
            self.db.query(
                ProjectModel.id,
                ProjectModel.title,
                ProjectModel.client,
                ProjectModel.delivery_date,
                UserProjectLinkModel.role,
                func.count(TaskModel.id).label("total_tasks"),
                func.sum(
                    case(
                        (
                            and_(
                                ColumnModel.position == subquery_positions.c.max_pos,
                                TaskModel.id.is_not(None),
                            ),
                            1,
                        ),
                        else_=0,
                    )
                ).label("completed_tasks"),
                func.sum(
                    case(
                        (
                            and_(
                                ColumnModel.position == subquery_positions.c.min_pos,
                                TaskModel.id.is_not(None),
                            ),
                            1,
                        ),
                        else_=0,
                    )
                ).label("not_started_tasks"),
            )
            .join(UserProjectLinkModel, ProjectModel.id == UserProjectLinkModel.project_id)
            .outerjoin(ColumnModel, ProjectModel.id == ColumnModel.project_id)
            .outerjoin(subquery_positions, ProjectModel.id == subquery_positions.c.project_id)
            .outerjoin(TaskModel, ColumnModel.id == TaskModel.column_id)
            .filter(UserProjectLinkModel.user_id == user_id)
            .group_by(ProjectModel.id, UserProjectLinkModel.role)
        )

    @staticmethod
    def _map_summaries(results) -> List[ProjectDashboardSummary]:
        return [
            ProjectDashboardSummary(
                id=row.id,
                title=row.title,
                client=row.client,
                role=RoleEnum(row.role),
                delivery_date=row.delivery_date,
                total_tasks=row.total_tasks,
                completed_tasks=row.completed_tasks or 0,
                not_started_tasks=row.not_started_tasks or 0,
            )
            for row in results
        ]

    @staticmethod
    def _status_expression(summaries) -> case:
        today = date.today()
        return case(
            (
                and_(
                    summaries.c.delivery_date < today,
                    summaries.c.completed_tasks != summaries.c.total_tasks,
                ),
                ProjectStatusEnum.DELAYED.value,
            ),
            (summaries.c.total_tasks == 0, ProjectStatusEnum.NOT_STARTED.value),
            (
                summaries.c.completed_tasks == summaries.c.total_tasks,
                ProjectStatusEnum.COMPLETED.value,
            ),
            (
                summaries.c.not_started_tasks == summaries.c.total_tasks,
                ProjectStatusEnum.NOT_STARTED.value,
            ),
            else_=ProjectStatusEnum.ACTIVE.value,
        )

    def get_user_project_summaries(self, user_id: str) -> List[ProjectDashboardSummary]:
        return self._map_summaries(self._summaries_query(user_id).all())

    def get_paginated_dashboard_projects(
        self,
        user_id: str,
        page: int = 1,
        page_size: int = 10,
        filters: Optional[ProjectFilters] = None,
    ) -> tuple[int, List[ProjectDashboardSummary]]:

        summaries = self._summaries_query(user_id).subquery()

        query = self.db.query(summaries)

        if filters:
            if filters.search:
                query = query.filter(summaries.c.title.ilike(f"%{filters.search.strip()}%"))

            if filters.role:
                query = query.filter(summaries.c.role == filters.role.value)

            if filters.status:
                query = query.filter(self._status_expression(summaries) == filters.status.value)

        total_items = query.count()

        offset = (page - 1) * page_size
        results = query.offset(offset).limit(page_size).all()

        return total_items, self._map_summaries(results)

    def get_by_id(self, project_id: str) -> Project:
        query = select(ProjectModel).where(ProjectModel.id == project_id)

        project = self.db.scalar(query)

        return map_project_model_to_entity(project) if project else None

    def get_project_members(self, project_id: str) -> List[ProjectMember]:
        results = (
            self.db.query(UserModel.id, UserModel.name, UserModel.email, UserProjectLinkModel.role)
            .join(UserProjectLinkModel, UserModel.id == UserProjectLinkModel.user_id)
            .filter(UserProjectLinkModel.project_id == project_id)
            .all()
        )

        return [
            ProjectMember(id=row.id, name=row.name, email=row.email, role=row.role)
            for row in results
        ]

    def get_project_board(
        self, project_id: str, filters: Optional[TaskFilters] = None
    ) -> Optional[ProjectBoard]:
        project_db = self.db.query(ProjectModel).filter(ProjectModel.id == project_id).first()

        if not project_db:
            return None

        column_rows = (
            self.db.query(ColumnModel)
            .filter(ColumnModel.project_id == project_id)
            .order_by(ColumnModel.position.asc())
            .all()
        )

        conditions: list = []
        apply_task_filters(conditions=conditions, filters=filters)
        conditions.append(TaskModel.column_id.in_([col.id for col in column_rows]))

        task_rows = (
            self.db.query(TaskModel)
            .options(joinedload(TaskModel.assignee))
            .filter(and_(*conditions))
            .order_by(TaskModel.created_at.asc())
            .all()
        )

        tasks_by_column: dict[str, List[TaskModel]] = {}
        for task in task_rows:
            tasks_by_column.setdefault(str(task.column_id), []).append(task)

        board_columns = []
        for col in column_rows:
            column_tasks = [
                TaskBoard(
                    id=str(task.id),
                    title=task.title,
                    description=task.description,
                    priority=TaskPriorityEnum(task.priority),
                    due_date=task.due_date,
                    assignee_id=str(task.assignee_id),
                    assignee_name=task.assignee.name if task.assignee else None,
                )
                for task in tasks_by_column.get(str(col.id), [])
            ]

            board_columns.append(
                ColumnBoard(
                    id=str(col.id), title=col.title, position=col.position, tasks=column_tasks
                )
            )

        return ProjectBoard(
            project_id=str(project_db.id), project_title=project_db.title, columns=board_columns
        )
