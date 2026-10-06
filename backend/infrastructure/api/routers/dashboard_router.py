from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from application.use_cases.dashboard.get import GetDashboardUseCase
from domain.utils.constants import Constants
from infrastructure.api.dependencies import (
    CurrentUser,
    ProjectRepositoryDep,
    TaskRepositoryDep,
    get_current_user,
)
from infrastructure.schemas.api_schema import ApiResponse
from infrastructure.schemas.dashboard_schema import DashboardResponseDTO, DueSoonTaskDTO


router = APIRouter(prefix="/dashboard", tags=["Dashboard"], dependencies=[Depends(get_current_user)])


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[DashboardResponseDTO],
    summary="Dashboard metrics",
    description=(
        "Returns the metrics of the authenticated user:\n\n"
        "- `totalProjects`: number of projects the user belongs to.\n"
        "- `projectsByStatus`: breakdown of those projects by derived status "
        "(`NOT_STARTED`, `ACTIVE`, `DELAYED`, `COMPLETED`). Always includes every "
        "status, even those with a zero total.\n"
        "- `totalTasks`: tasks assigned to the user.\n"
        "- `completedTasks`: tasks assigned to the user sitting in the completed column of their project.\n"
        "- `tasksDueSoon`: tasks assigned to the user that are not completed and are due between today and the next 7 days.\n"
        "- `weeklyPerformance`: exactly 7 entries, from 6 days ago to today, with tasks created and completed per day. "
        "Days without activity are returned with 0.\n\n"
        "The scope is always the authenticated user; no user identifier is accepted in the path."
    ),
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing, invalid or expired token.",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Unexpected error while computing the metrics.",
        },
    },
)
def get_dashboard_metrics(
    current_user: CurrentUser,
    project_repository: ProjectRepositoryDep,
    task_repository: TaskRepositoryDep,
):
    try:
        use_case = GetDashboardUseCase(
            project_repository=project_repository,
            task_repository=task_repository
        )

        dashboard_metrics = use_case.execute(user_id=current_user.id)

        return ApiResponse(
            ok=True,
            message="Dashboard metrics",
            data=DashboardResponseDTO.from_entity(dashboard_metrics)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=Constants.UNEXPECTED_ERROR + str(e)
        )


@router.get(
    path="/tasks/due-soon",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[List[DueSoonTaskDTO]],
    summary="Tasks due soon",
    description=(
        "Returns the tasks behind the `tasksDueSoon` metric, so the dashboard can list them.\n\n"
        "Includes only tasks assigned to the authenticated user that are **not completed** "
        "and whose `dueDate` falls between today and the next 7 days. Completed and already "
        "overdue tasks are excluded. Results are ordered by due date ascending.\n\n"
        "Returns an empty list when there is nothing due soon."
    ),
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "description": "Missing, invalid or expired token.",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Unexpected error while loading the tasks.",
        },
    },
)
def get_due_soon_tasks(
    current_user: CurrentUser,
    project_repository: ProjectRepositoryDep,
    task_repository: TaskRepositoryDep,
):
    try:
        use_case = GetDashboardUseCase(
            project_repository=project_repository,
            task_repository=task_repository
        )

        due_soon_tasks = use_case.execute_due_soon_tasks(user_id=current_user.id)

        return ApiResponse(
            ok=True,
            message="Tasks due soon",
            data=[DueSoonTaskDTO.from_entity(task) for task in due_soon_tasks]
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=Constants.UNEXPECTED_ERROR + str(e)
        )
