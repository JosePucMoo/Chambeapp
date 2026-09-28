
from infrastructure.mappers.project_mappers import map_project_entity_to_model, map_project_model_to_entity
from domain.entities.project import Project
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