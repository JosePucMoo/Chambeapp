from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Query, status

from application.use_cases.project.get import GetProjectUseCase
from domain.exceptions.not_found_exception import NotFoundException
from infrastructure.schemas.pagination_schema import PaginatedResponseDTO
from domain.exceptions.cannot_create_exception import CannotCreateException
from domain.utils.constants import Constants
from application.use_cases.project.create import CreateProjectUseCase
from infrastructure.api.dependencies import ColumnRepositoryDep, CurrentUser, ProjectRepositoryDep, UserProjectLinkRepositoryDep, get_current_user
from infrastructure.schemas.api_schema import ApiResponse
from infrastructure.schemas.project_schema import CreateProjectDTO, ProjectBoardDTO, ProjectMemberResponseDTO, ProjectResponseDTO, ProjectDashboardSummaryDTO
from infrastructure.mappers.project_mappers import map_create_project_dto_to_entity


router = APIRouter(prefix="/projects", tags=["Projects"], dependencies=[Depends(get_current_user)])

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
        ge=5,
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

@router.get("/{project_id}/members", status_code=status.HTTP_200_OK, response_model=ApiResponse[List[ProjectMemberResponseDTO]])
def get_project_members(
    project_id: str,
    repositoy: ProjectRepositoryDep
):
    try:
        use_case = GetProjectUseCase(repository=repositoy)
        project_members = use_case.execute_get_project_members(project_id)
        data = [ProjectMemberResponseDTO.model_validate(member) for member in project_members]
        return ApiResponse(
            ok=True,
            message="Lista de miembros del proyecto",
            data=data
        )
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=Constants.UNEXPECTED_ERROR + str(e)
        )

@router.get("/{project_id}/board", status_code=status.HTTP_200_OK, response_model=ApiResponse[ProjectBoardDTO])
def get_project_board(
    project_id: str,
    repositoy: ProjectRepositoryDep
):
    try:
        use_case = GetProjectUseCase(repository=repositoy)
        project_board = use_case.execute_get_project_board(project_id)
        data = ProjectBoardDTO.from_entity(project_board)
        return ApiResponse(
            ok=True,
            message="Tablero del proyecto con columnas y tareas",
            data=data
        )
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=Constants.UNEXPECTED_ERROR + str(e)
        )

@router.get("/{project_id}", status_code=status.HTTP_200_OK, response_model=ApiResponse[ProjectResponseDTO])
def get_project(
    project_id: str,
    repositoy: ProjectRepositoryDep
):
    try:
        use_case = GetProjectUseCase(repository=repositoy)
        project = use_case.execute(project_id)
        data = ProjectResponseDTO.model_validate(project)
        return ApiResponse(
            ok=True,
            message=f'Proyecto: {data.title}',
            data=data
        )
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=Constants.UNEXPECTED_ERROR + str(e)
        )