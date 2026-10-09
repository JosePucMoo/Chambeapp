from typing import Annotated, List, Optional
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status

from application.use_cases.task.create import CreateTaskUseCase
from application.use_cases.task.change_column import ChangeColumnUseCase
from application.use_cases.task.delete import DeleteTaskUseCase
from application.use_cases.task.get import GetTaskUseCase
from application.use_cases.task.update import UpdateTaskUseCase
from infrastructure.schemas.pagination_schema import PaginatedResponseDTO
from domain.entities.enums import TaskPriorityEnum
from domain.entities.task import TaskFilters
from domain.exceptions.not_found_exception import NotFoundException
from domain.exceptions.cannot_create_exception import CannotCreateException
from domain.exceptions.cannot_update_exception import CannotUpdateException
from domain.utils.constants import Constants
from infrastructure.mappers.task_mappers import (
    map_task_dto_to_entity,
    map_update_task_dto_to_entity,
)
from infrastructure.api.dependencies import (
    ColumnRepositoryDep,
    CurrentUser,
    ProjectRepositoryDep,
    TaskRepositoryDep,
    get_current_user,
)
from infrastructure.schemas.api_schema import ApiResponse
from infrastructure.schemas.task_schema import (
    BulkDeleteTasksDTO,
    CalendarTaskDTO,
    TaskDashboardSummaryDTO,
    TaskDetailDTO,
    TaskMoveDTO,
    TaskResponseDTO,
    CreateTaskDTO,
    UpdateTaskDTO,
)


router = APIRouter(prefix="/tasks", tags=["Tasks"], dependencies=[Depends(get_current_user)])


@router.post(
    path="/{project_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=ApiResponse[TaskResponseDTO],
)
def create_task(
    project_id: str,
    task_data: CreateTaskDTO,
    repository: TaskRepositoryDep,
    project_repository: ProjectRepositoryDep,
    column_repository: ColumnRepositoryDep,
):
    try:
        use_case = CreateTaskUseCase(
            repository=repository,
            project_repository=project_repository,
            column_repository=column_repository,
        )
        task = use_case.execute(project_id, map_task_dto_to_entity(task_data))
        return ApiResponse(
            ok=True, message="Tarea creado con éxito", data=TaskResponseDTO.model_validate(task)
        )
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except CannotCreateException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=Constants.UNEXPECTED_ERROR + str(e),
        )


@router.get(
    path="/calendar",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[List[CalendarTaskDTO]],
)
def get_calendar_tasks(
    current_user: CurrentUser,
    repository: TaskRepositoryDep,
    start_date: Annotated[date, Query(description="Fecha de inicio del rango (inclusive)")],
    end_date: Annotated[date, Query(description="Fecha de fin del rango (inclusive)")],
    priority: Annotated[Optional[TaskPriorityEnum], Query()] = None,
    column_title: Annotated[Optional[str], Query(max_length=100)] = None,
    project_id: Annotated[Optional[str], Query()] = None,
    search: Annotated[Optional[str], Query(max_length=50)] = None,
):
    try:
        use_case = GetTaskUseCase(repository=repository)

        filters = TaskFilters(
            priority=priority, column_title=column_title, project_id=project_id, search=search
        )

        tasks = use_case.execute_calendar(
            user_id=current_user.id, start_date=start_date, end_date=end_date, filters=filters
        )

        return ApiResponse(
            ok=True,
            message="Tareas del periodo consultado",
            data=[CalendarTaskDTO.model_validate(task) for task in tasks],
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=Constants.UNEXPECTED_ERROR + str(e),
        )


@router.get("/{task_id}", status_code=status.HTTP_200_OK, response_model=ApiResponse[TaskDetailDTO])
def get_task(task_id: str, current_user: CurrentUser, repository: TaskRepositoryDep):
    try:
        use_case = GetTaskUseCase(repository=repository)
        task = use_case.execute_detail(user_id=current_user.id, task_id=task_id)

        return ApiResponse(
            ok=True, message=f"Tarea: {task.title}", data=TaskDetailDTO.model_validate(task)
        )
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=Constants.UNEXPECTED_ERROR + str(e),
        )


@router.put(
    path="/{task_id}", status_code=status.HTTP_200_OK, response_model=ApiResponse[TaskResponseDTO]
)
def update_task(
    task_id: str,
    update_data: UpdateTaskDTO,
    current_user: CurrentUser,
    repository: TaskRepositoryDep,
    project_repository: ProjectRepositoryDep,
):
    try:
        use_case = UpdateTaskUseCase(repository=repository, project_repository=project_repository)

        updated_task = use_case.execute(
            user_id=current_user.id,
            task_id=task_id,
            task_data=map_update_task_dto_to_entity(update_data, task_id),
        )

        return ApiResponse(
            ok=True,
            message="Tarea actualizada con éxito",
            data=TaskResponseDTO.model_validate(updated_task),
        )
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except CannotUpdateException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=Constants.UNEXPECTED_ERROR + str(e),
        )


@router.delete(path="/{task_id}", status_code=status.HTTP_200_OK, response_model=ApiResponse)
def delete_task(task_id: str, current_user: CurrentUser, repository: TaskRepositoryDep):
    try:
        use_case = DeleteTaskUseCase(repository=repository)
        use_case.execute(user_id=current_user.id, task_id=task_id)

        return ApiResponse(ok=True, message="Tarea eliminada con éxito", data=None)
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=Constants.UNEXPECTED_ERROR + str(e),
        )


@router.patch(
    path="/{task_id}/move",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[TaskResponseDTO],
)
def move_task(
    task_id: str,
    update_data: TaskMoveDTO,
    current_user: CurrentUser,
    repository: TaskRepositoryDep,
    column_repository: ColumnRepositoryDep,
):
    try:
        use_case = ChangeColumnUseCase(repository=repository, column_repository=column_repository)

        updated_task = use_case.execute(
            user_id=current_user.id, task_id=task_id, column_id=update_data.column_id
        )

        return ApiResponse(
            ok=True, message="Tarea cambiada de columna con éxito", data=updated_task
        )
    except NotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except CannotUpdateException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=Constants.UNEXPECTED_ERROR + str(e),
        )


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[PaginatedResponseDTO[TaskDashboardSummaryDTO]],
)
def get_paginated_summary_projects(
    current_user: CurrentUser,
    repository: TaskRepositoryDep,
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=5, le=50)] = 10,
    priority: Annotated[Optional[TaskPriorityEnum], Query()] = None,
    column_title: Annotated[Optional[str], Query(max_length=100)] = None,
    project_id: Annotated[Optional[str], Query()] = None,
    search: Annotated[Optional[str], Query(max_length=50)] = None,
):
    try:
        use_case = GetTaskUseCase(
            repository=repository,
        )
        filters = TaskFilters(
            priority=priority, column_title=column_title, project_id=project_id, search=search
        )
        [total_count, tasks_summary] = use_case.execute_paginated_summary(
            user_id=current_user.id, page=page, page_size=page_size, filters=filters
        )

        data = PaginatedResponseDTO.create(
            total_count=total_count, data=tasks_summary, page=page, page_size=page_size
        )
        return ApiResponse(ok=True, message="Lista de mis tareas", data=data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=Constants.UNEXPECTED_ERROR + str(e),
        )


@router.delete(path="/", status_code=status.HTTP_200_OK, response_model=ApiResponse[List[str]])
def delete_tasks(
    bulk_data: BulkDeleteTasksDTO, current_user: CurrentUser, repository: TaskRepositoryDep
):
    try:
        use_case = DeleteTaskUseCase(repository=repository)
        deleted_ids = use_case.execute_many(user_id=current_user.id, task_ids=bulk_data.task_ids)

        return ApiResponse(
            ok=True, message=f"{len(deleted_ids)} tarea(s) eliminada(s) con éxito", data=deleted_ids
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=Constants.UNEXPECTED_ERROR + str(e),
        )
