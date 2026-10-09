from fastapi import APIRouter

from infrastructure.api.routers.auth_router import router as auth_router
from infrastructure.api.routers.project_router import router as project_router
from infrastructure.api.routers.task_router import router as task_router
from infrastructure.api.routers.dashboard_router import router as dashboard_router
from infrastructure.api.routers.invitation_router import router as invitation_router


router = APIRouter()

router.include_router(auth_router)
router.include_router(project_router)
router.include_router(task_router)
router.include_router(dashboard_router)
router.include_router(invitation_router)
