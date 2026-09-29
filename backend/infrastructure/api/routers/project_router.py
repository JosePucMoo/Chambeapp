from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status

from application.use_cases.project.get import GetProjectUseCase
from infrastructure.schemas.pagination_schema import PaginatedResponseDTO
from domain.exceptions.cannot_create_exception import CannotCreateException
from domain.utils.constants import Constants
from application.use_cases.project.create import CreateProjectUseCase
from infrastructure.api.dependencies import ColumnRepositoryDep, CurrentUser, ProjectRepositoryDep, TaskRepositoryDep, UserProjectLinkRepositoryDep
from infrastructure.schemas.api_schema import ApiResponse
from infrastructure.schemas.project_schema import CreateProjectDTO, ProjectResponseDTO, ProjectDashboardSummaryDTO
from infrastructure.mappers.project_mappers import map_create_project_dto_to_entity


router = APIRouter(prefix="/projects", tags=["Projects"])

@router.post("/", response_model=ApiResponse[ProjectResponseDTO], status_code=status.HTTP_201_CREATED)
def create_project(
    project_data: CreateProjectDTO, 
    repository: ProjectRepositoryDep,
    column_repository: ColumnRepositoryDep,
    user_project_link_repository: UserProjectLinkRepositoryDep,
    current_user: CurrentUser
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

    
@router.get("/", status_code=status.HTTP_200_OK, response_model=ApiResponse[PaginatedResponseDTO[ProjectDashboardSummaryDTO]])
def get_paginated_summary_projects(
    curren_user: CurrentUser,
    repository: ProjectRepositoryDep,
    page: Annotated[int, Query(
        ge=1
    )] = 1,
    page_size: Annotated[int, Query(
        ge=10,
        le=50
    )] = 10,
):
    try:
        use_case = GetProjectUseCase(
            repository=repository,
        )
        [total_count, projects_summary] = use_case.execute_paginated_summary(user_id=curren_user.id, page=page, page_size=page_size)

        data = PaginatedResponseDTO.create(
            total_count=total_count,
            data=projects_summary,
            page=page,
            page_size=page_size
        )
        return ApiResponse(
            ok=True,
            message="Lista de projectos",
            data=data
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=Constants.UNEXPECTED_ERROR + str(e)
        )