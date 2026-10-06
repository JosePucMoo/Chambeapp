from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class BaseSchema(BaseModel):
    """
    Clase base para todos los esquemas de Pydantic en la aplicación.
    Convierte automáticamente snake_case (Python) a camelCase (JSON/Frontend).
    """

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
    )
