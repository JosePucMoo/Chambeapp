import logging
from contextlib import asynccontextmanager
import os
from venv import logger
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from pydantic.alias_generators import to_camel
from infrastructure.schemas.api_schema import ErrorDetail, ErrorResponse
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

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_details = []
    
    for err in exc.errors():
        loc = err.get("loc", ())
        field = to_camel(str(loc[-1])) if len(loc) > 1 else "Formulario"
        raw_msg = err.get("msg", "Dato inválido").replace("Value error, ", "")
        
        error_details.append(
            ErrorDetail(
                type="VALIDATION_ERROR",
                message=f"{field}: {raw_msg}"
            )
        )
    
    response_body = ErrorResponse(detail=error_details)
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=response_body.model_dump(exclude_none=True)
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    error_detail = ErrorDetail(
        type=f"HTTP_{exc.status_code}_ERROR", 
        message=str(exc.detail)
    )

    error_response = ErrorResponse(detail=[error_detail])
    
    headers = getattr(exc, "headers", None)
    
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.model_dump(exclude_none=True),
        headers=headers
    )

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

origins = [
    os.getenv('FRONTEND_URL')
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.openapi = custom_openapi

app.include_router(router)