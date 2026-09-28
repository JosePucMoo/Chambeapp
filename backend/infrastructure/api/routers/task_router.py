

from fastapi import APIRouter, HTTPException, status

from application.use_cases.task.create import CreateTaskUseCase
from domain.exceptions.cannot_create_exception import CannotCreateException
from domain.utils.constants import Constants
from infrastructure.mappers.task_mappers import map_task_dto_to_entity
from infrastructure.api.dependencies import TaskRepositoryDep
from infrastructure.schemas.api_schema import ApiResponse
from infrastructure.schemas.task_schema import TaskResponseDTO, CreateTaskDTO


router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post(path="/", status_code=status.HTTP_201_CREATED, response_model=ApiResponse[TaskResponseDTO])
def create_task(
    task_data: CreateTaskDTO,
    repository: TaskRepositoryDep
):
    try:
        use_case = CreateTaskUseCase(repository=repository)
        task = use_case.execute(
            map_task_dto_to_entity(task_data)
        )
        return ApiResponse(
            ok=True, 
            message="Tarea creado con éxito",
            data=TaskResponseDTO.model_validate(task)
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