from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from domain.exceptions.cannot_create_exception import CannotCreateException
from domain.utils.constants import Constants
from infrastructure.schemas.auth_schema import UserResponseDTO
from domain.repositories.column_repository import ColumnRepository
from domain.repositories.user_project_link_repository import UserProjectLinkRepository
from domain.repositories.project_repository import ProjectRepository
from application.use_cases.project.create import CreateProjectUseCase
from infrastructure.api.dependencies import get_column_repository, get_current_user, get_project_repository, get_user_project_link_repository
from infrastructure.schemas.api_schema import ApiResponse
from infrastructure.schemas.project_schema import CreateProjectDTO, ProjectResponseDTO
from infrastructure.mappers.project_mappers import map_create_project_dto_to_entity


router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("/", response_model=ApiResponse[ProjectResponseDTO], status_code=status.HTTP_201_CREATED)
def create_project(
    project_data: CreateProjectDTO, 
    repository: Annotated[ProjectRepository, Depends(get_project_repository)],
    column_repository: Annotated[ColumnRepository, Depends(get_column_repository)],
    user_project_link_repository: Annotated[UserProjectLinkRepository, Depends(get_user_project_link_repository)],
    current_user: Annotated[UserResponseDTO, Depends(get_current_user)]
    ):
    try:
        use_case = CreateProjectUseCase(
            repository=repository, 
            column_repository=column_repository,
            user_project_link_repository=user_project_link_repository
        )
        project = use_case.execute(
            project_data=map_create_project_dto_to_entity(project_data),
            user_id=current_user.id
        )
        data = ProjectResponseDTO.model_validate(project)
        return ApiResponse(
            ok=True,
            message="Proyecto creado con éxito",
            data=data
        )
    except CannotCreateException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=Constants.UNEXPECTED_ERROR + str(e)
        )

    
