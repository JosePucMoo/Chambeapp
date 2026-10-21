from sqlalchemy.orm import Session

from infrastructure.repositories.task_repository_impl import TaskRepositoryImpl
from tests.integration.factories import Factories


class TestTaskRepository:
    def test_create_and_get_by_id(self, db_session: Session):
        owner = Factories.create_user(db_session, email="task_owner@test.com")
        project = Factories.create_project(db_session, owner_user=owner)
        columns = Factories.create_columns(db_session, project)
        task = Factories.create_task(db_session, columns[0], owner)
        repo = TaskRepositoryImpl(db_session)
        fetched = repo.get_by_id(task.id)
        assert fetched is not None
        assert fetched.title == "Tarea"

    def test_delete(self, db_session: Session):
        owner = Factories.create_user(db_session, email="task_owner2@test.com")
        project = Factories.create_project(db_session, owner_user=owner)
        columns = Factories.create_columns(db_session, project)
        task = Factories.create_task(db_session, columns[0], owner)
        repo = TaskRepositoryImpl(db_session)
        result = repo.delete(owner.id, task.id)
        assert result is True
        fetched = repo.get_by_id(task.id)
        assert fetched is None
