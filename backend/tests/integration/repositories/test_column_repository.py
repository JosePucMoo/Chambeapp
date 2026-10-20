

from sqlalchemy.orm import Session

from domain.entities.enums import ColumnDefaultEnum
from domain.entities.column import Column
from tests.integration.factories import Factories
from infrastructure.repositories.column_repository_impl import ColumnRepositoryImpl


class TestColumnRepository:
    def test_create_default_columns(self, db_session: Session):
        repository = ColumnRepositoryImpl(db_session)
        
        user = Factories.create_user(session=db_session)
        
        project = Factories.create_project(session=db_session, owner_user=user, title="New Project", client="My project", description="This a project for test")
        
        column_1= Column(title=ColumnDefaultEnum.TO_DO, position=1, project_id=project.id)
        column_2= Column(title=ColumnDefaultEnum.IN_PROGRESS, position=2, project_id=project.id)
        column_3= Column(title=ColumnDefaultEnum.COMPLETED, position=3, project_id=project.id)
        
        columns = [column_1, column_2, column_3]
        
        created_columns = repository.create_default_columns(columns)
        
        assert len(created_columns) == 3
        assert created_columns[0].title == "Por hacer"
        
    def test_get_first_column_by_project(self, db_session: Session):
        user = Factories.create_user(session=db_session)
        
        project = Factories.create_project(session=db_session, owner_user=user, title="New Project", client="My project", description="This a project for test")
        
        Factories.create_default_columns(db_session, project=project)
        
        repository = ColumnRepositoryImpl(db=db_session)
        
        first_column = repository.get_the_first_column_by_project(project.id)
        
        assert first_column is not None
        assert first_column.position == 1
        
        