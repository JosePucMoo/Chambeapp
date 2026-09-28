

from domain.entities.project import Project
from infrastructure.db.models.project_model import ProjectModel
from infrastructure.schemas.project_schema import CreateProjectDTO

def map_create_project_dto_to_entity(project: CreateProjectDTO) -> Project:
    return Project(
        title=project.title,
        description=project.description,
        client=project.client,
        delivery_date=project.delivery_date
    )

def map_project_entity_to_model(project: Project) -> ProjectModel:
    return ProjectModel(
        id=project.id,
        title=project.title,
        description=project.description,
        client=project.client,
        delivery_date=project.delivery_date
    )

def map_project_model_to_entity(project: ProjectModel) -> Project:
    return Project(
        id=project.id,
        title=project.title,
        description=project.description,
        client=project.client,
        delivery_date=project.delivery_date
    )