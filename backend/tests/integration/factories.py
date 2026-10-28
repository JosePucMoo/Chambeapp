from datetime import datetime, timedelta
import uuid
from sqlalchemy.orm import Session

from domain.entities.enums import RoleEnum, TaskPriorityEnum
from domain.entities.user import User
from domain.entities.project import Project
from domain.entities.column import Column
from domain.entities.task import Task
from domain.entities.user_project_link import UserProjectLink
from infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from infrastructure.repositories.project_repository_impl import ProjectRepositoryImpl
from infrastructure.repositories.user_project_link_repository_impl import (
    UserProjectLinkRepositoryImpl,
)
from infrastructure.repositories.task_repository_impl import TaskRepositoryImpl
from infrastructure.mappers.column_mappers import (
    map_column_entity_to_model,
    map_column_model_to_entity,
)


class Factories:
    @staticmethod
    def create_user(
        session: Session,
        name: str = "Test",
        email: str = "test@test.com",
        password: str = "hashed",
        is_verified: bool = False,
        token: str = None,
    ):
        repo = UserRepositoryImpl(session)
        if email is None:
            email = f"{uuid.uuid4()}@test.com"
        user = User(name=name, email=email, password=password, is_verified=is_verified, token=token)
        return repo.create(user)

    @staticmethod
    def create_project(
        session: Session,
        owner_user: User,
        title: str = "Proyecto",
        description: str = "Desc",
        client: str = "Cliente",
        delivery_date: datetime = datetime.now() + timedelta(days=10),
    ):
        repo = ProjectRepositoryImpl(session)
        project = Project(
            title=title, description=description, client=client, delivery_date=delivery_date
        )
        created_project = repo.create(project)
        link_repo = UserProjectLinkRepositoryImpl(session)
        link = UserProjectLink(
            role=RoleEnum.OWNER, user_id=owner_user.id, project_id=created_project.id
        )
        link_repo.create(link)
        return created_project

    @staticmethod
    def create_columns(
        session: Session, project: Project, titles=("Por hacer", "En progreso", "Completado")
    ):
        created = []
        for idx, title in enumerate(titles):
            real_position = idx + 1
            column = Column(title=title, position=real_position, project_id=project.id)
            model = map_column_entity_to_model(column)
            session.add(model)
            session.commit()
            session.refresh(model)
            created.append(map_column_model_to_entity(model))
        return created

    @staticmethod
    def create_default_columns(
        session: Session, project: Project, titles=("Por hacer", "En progreso", "Completado")
    ):
        return Factories.create_columns(session, project, titles)

    @staticmethod
    def create_task(
        session: Session,
        column: Column,
        assignee: User,
        title: str = "Tarea",
        description: str = "Desc",
        priority: TaskPriorityEnum = TaskPriorityEnum.MEDIUM,
        due_date: datetime = datetime.now() + timedelta(days=10),
    ):
        repo = TaskRepositoryImpl(session)
        task = Task(
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            assignee_id=assignee.id,
            column_id=column.id,
        )
        return repo.create(task)
