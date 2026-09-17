
from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator
from typing import Optional
from typing_extensions import Self

class CreateUserDTO(BaseModel):
    name: str = Field(
        ..., 
        min_length=2, 
        max_length=50, 
        strip_whitespace=True,
        description="Nombre completo del usuario"
    )
    email: EmailStr
    password: str = Field(..., min_length=8)
    password_confirm: str

    @model_validator(mode='after')
    def verify_passwords_match(self) -> Self:
        if self.password != self.password_confirm:
            raise ValueError("Las contraseñas no coinciden")
        return self

class UpdateUserDTO(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    is_verified: Optional[str] = None

class LoginUserDTO(BaseModel):
    email: EmailStr
    password: str

class UserResponseDTO(BaseModel):
    id: str
    name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)

    
    