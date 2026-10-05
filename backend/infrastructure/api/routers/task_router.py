

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from application.use_cases.task.create import CreateTaskUseCase
from application.use_cases.task.change_column import ChangeColumnUseCase
from application.use_cases.task.get import GetTaskUseCase
from infrastructure.schemas.pagination_schema import PaginatedResponseDTO
from domain.exceptions.not_found_exception import NotFoundException
from domain.exceptions.cannot_create_exception import CannotCreateException
from domain.utils.constants import Constants
from infrastructure.mappers.task_mappers import map_task_dto_to_entity
from infrastructure.api.dependencies import ColumnRepositoryDep, CurrentUser, ProjectRepositoryDep, TaskRepositoryDep, get_current_user
from infrastructure.schemas.api_schema import ApiResponse
from infrastructure.schemas.task_schema import TaskDashboardSummaryDTO, TaskMoveDTO, TaskResponseDTO, CreateTaskDTO


router = APIRouter(prefix="/tasks", tags=["Tasks"], dependencies=[Depends(get_current_user)])

@router.post(path="/{project_id}", status_code=status.HTTP_201_CREATED, response_model=ApiResponse[TaskResponseDTO])
def create_task(
    project_id: str,
    task_data: CreateTaskDTO,
    repository: TaskRepositoryDep,
    project_repository: ProjectRepositoryDep,
    column_repository: ColumnRepositoryDep
):
    try:
        use_case = CreateTaskUseCase(repository=repository, project_repository=project_repository, column_repository=column_repository)
        task = use_case.execute(
            project_id,
            map_task_dto_to_entity(task_data)
        )
        return ApiResponse(
            ok=True, 
            message="Tarea creado con éxito",
            data=TaskResponseDTO.model_validate(task)
        )
    except NotFoundException as e:
        raise HTTPException(
           status_code=status.HTTP_404_NOT_FOUND,
           detail=str(e)
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

@router.patch(path="/{task_id}/move", status_code=status.HTTP_200_OK, response_model=ApiResponse[TaskResponseDTO])
def move_task(
    task_id: str,
    update_data: TaskMoveDTO,
    repository: TaskRepositoryDep,
    column_repository: ColumnRepositoryDep
):
    try:
        use_case = ChangeColumnUseCase(
            repository=repository,
            column_repository=column_repository
            )

        updated_task = use_case.execute(task_id, update_data.column_id)

        return ApiResponse(
            ok=True,
            message="Tarea cambiada de columna con éxito",
            data=updated_task
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

@router.get("/", status_code=status.HTTP_200_OK, response_model=ApiResponse[PaginatedResponseDTO[TaskDashboardSummaryDTO]])
def get_paginated_summary_projects(
    current_user: CurrentUser,
    repository: TaskRepositoryDep,
    page: Annotated[int, Query(
        ge=1
    )] = 1,
    page_size: Annotated[int, Query(
        ge=5,
        le=50
    )] = 10,
):
    try:
        use_case = GetTaskUseCase(
            repository=repository,
        )
        [total_count, tasks_summary] = use_case.execute_paginated_summary(user_id=current_user.id, page=page, page_size=page_size)

        data = PaginatedResponseDTO.create(
            total_count=total_count,
            data=tasks_summary,
            page=page,
            page_size=page_size
        )
        return ApiResponse(
            ok=True,
            message="Lista de mis tareas",
            data=data
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=Constants.UNEXPECTED_ERROR + str(e)
        )