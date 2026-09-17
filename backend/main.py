import logging
from contextlib import asynccontextmanager
from venv import logger

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from infrastructure.api.routers.router import router
from infrastructure.db.database import engine
from infrastructure.db.models.base_model import Base

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Iniciando aplicación Chambeapp...")
    Base.metadata.create_all(bind=engine)
    logger.info("Base de datos inicializada")

    yield

    logger.info("Deteniendo aplicación...")
    logger.info("Aplicación detenida correctamente")


app = FastAPI(lifespan=lifespan)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Chambeapp API",
        version="1.0.0",
        contact={
            "name": "José Puc",
            "email": "pucjl07@gmail.com",
            "url": "https://github.com/JosePucMoo",
        },
        summary="RESTful API for the Chambeapp task manager",
        routes=app.routes,
        # tags=openapi_tags,
    )
    openapi_schema["info"]["x-logo"] = {"url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"}
    openapi_schema["info"]["x-contacts"] = [
        {"name": "Jose Puc", "email": "pucjl07@gmail.com"},
    ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

app.include_router(router)