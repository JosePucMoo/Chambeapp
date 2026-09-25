from datetime import datetime, timezone
from typing import Generic, TypeVar, Optional
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )

    ok: bool
    message: str
    data: T = None

class ErrorDetail(BaseModel):
    type: str
    message: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class ErrorResponse(BaseModel):
    detail: list[ErrorDetail]