

from sqlalchemy.orm import Session

from tests.integration.factories import Factories
from infrastructure.repositories.column_repository_impl import ColumnRepositoryImpl


class TestColumnRepository:
    
    def test_get_first_column(self, db_session: Session):
        owner = Factories.create_user(db_session)
        project = Factories.create_project(db_session, owner_user=owner)
        columns = Factories.create_columns(db_session, project, titles=("A", "B", "C"))

        repo = ColumnRepositoryImpl(db_session)
        first = repo.get_the_first_column_by_project(project.id)
        assert first is not None
        assert first.position == 1 or first.position == columns[0].position
    
        