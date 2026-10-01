
from typing import List

from sqlalchemy import and_, case, func, select

from infrastructure.db.models.user_model import UserModel
from domain.entities.enums import RoleEnum
from infrastructure.db.models.column_model import ColumnModel
from infrastructure.db.models.project_model import ProjectModel
from infrastructure.db.models.user_project_link_model import UserProjectLinkModel
from infrastructure.db.models.task_model import TaskModel
from infrastructure.mappers.project_mappers import map_project_entity_to_model, map_project_model_to_entity
from domain.entities.project import Project, ProjectDashboardSummary, ProjectMember
from domain.repositories.project_repository import ProjectRepository
from sqlalchemy.orm import Session

class ProjectRepositoryImpl(ProjectRepository):
    def __init__(self, db: Session):
        self.db = db

    def create(self, project: Project)-> Project:
        project_model = map_project_entity_to_model(project)

        self.db.add(project_model)
        self.db.commit()
        self.db.refresh(project_model)
        
        return map_project_model_to_entity(project_model)

    def get_paginated_dashboard_projects(
            self, user_id: int, page: int = 1, page_size: int = 10
        ) -> tuple[int, List[ProjectDashboardSummary]]:
            
            subquery_positions = (
                self.db.query(
                    ColumnModel.project_id,
                    func.max(ColumnModel.position).label("max_pos"),
                    func.min(ColumnModel.position).label("min_pos")
                )
                .group_by(ColumnModel.project_id)
                .subquery()
            )
    
            query = (
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
                                    TaskModel.id.is_not(None)
                                ), 1
                            ), 
                            else_=0
                        )
                    ).label("completed_tasks"),

                    func.sum(
                        case(
                            (
                                and_(
                                    ColumnModel.position == subquery_positions.c.min_pos,
                                    TaskModel.id.is_not(None)
                                ),
                            1), 
                            else_=0
                        )
                    ).label("not_started_tasks")
                )
                
                .join(UserProjectLinkModel, ProjectModel.id == UserProjectLinkModel.project_id)
                
                .outerjoin(ColumnModel, ProjectModel.id == ColumnModel.project_id)
                .outerjoin(subquery_positions, ProjectModel.id == subquery_positions.c.project_id)
                .outerjoin(TaskModel, ColumnModel.id == TaskModel.column_id)
                
                .filter(UserProjectLinkModel.user_id == user_id)
                
                .group_by(ProjectModel.id, UserProjectLinkModel.role)
            )
    
            total_items = (
                self.db.query(func.count(ProjectModel.id))
                .join(UserProjectLinkModel, ProjectModel.id == UserProjectLinkModel.project_id)
                .filter(UserProjectLinkModel.user_id == user_id)
                .scalar()
            )
    
            offset = (page - 1) * page_size
            results = query.offset(offset).limit(page_size).all()
    
            projects = [
                ProjectDashboardSummary(
                    id=row.id,
                    title=row.title,
                    client=row.client,
                    
                    role=RoleEnum(row.role), 
                    
                    delivery_date=row.delivery_date,
                    total_tasks=row.total_tasks,
                    completed_tasks=row.completed_tasks or 0,
                    not_started_tasks=row.not_started_tasks or 0
                )
                for row in results
            ]
    
            return total_items, projects

    def get_by_id(self, project_id: str) -> Project:
        query = select(ProjectModel).where(ProjectModel.id == project_id)

        project = self.db.scalar(query)

        return map_project_model_to_entity(project) if project else None

    def get_project_members(self, project_id: str) -> List[ProjectMember]:
        results = (
            self.db.query(
                UserModel.id,
                UserModel.name,
                UserModel.email,
            )
            .join(UserProjectLinkModel, UserModel.id == UserProjectLinkModel.user_id)
            .filter(UserProjectLinkModel.project_id == project_id)
            .all()
        )

        return [
            ProjectMember(
                 id=row.id,
                 name=row.name,
                 email=row.email
            )
            for row in results
        ]