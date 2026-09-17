
from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator
from typing import Optional
from typing_extensions import Self

class UserBaseDTO(BaseModel):
    name: str
    email: EmailStr

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

class UpdateProfileUserDTO(BaseModel):
    name: str = Field(
        ..., 
        min_length=2, 
        max_length=50, 
        strip_whitespace=True,
        description="Nombre completo del usuario"
    )

class LoginUserDTO(BaseModel):
    email: EmailStr
    password: str

class UserResponseDTO(UserBaseDTO):
    id: str

    model_config = ConfigDict(from_attributes=True)

    
    