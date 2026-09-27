
from fastapi import APIRouter

from infrastructure.api.routers.auth_router import router as auth_router


router = APIRouter()

router.include_router(auth_router)