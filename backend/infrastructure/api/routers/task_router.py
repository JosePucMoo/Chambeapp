

from fastapi import APIRouter, Depends, HTTPException, status

from application.use_cases.task.create import CreateTaskUseCase
from application.use_cases.task.change_column import ChangeColumnUseCase
from domain.exceptions.not_found_exception import NotFoundException
from domain.exceptions.cannot_create_exception import CannotCreateException
from domain.utils.constants import Constants
from infrastructure.mappers.task_mappers import map_task_dto_to_entity
from infrastructure.api.dependencies import ColumnRepositoryDep, ProjectRepositoryDep, TaskRepositoryDep, get_current_user
from infrastructure.schemas.api_schema import ApiResponse
from infrastructure.schemas.task_schema import TaskMoveDTO, TaskResponseDTO, CreateTaskDTO


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
