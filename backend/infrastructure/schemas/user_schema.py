
from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator
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

class ChangePasswordUserDTO(BaseModel):
    old_password: str = Field(...)
    new_password: str = Field(..., min_length=8, description="Nueva contraseña")

    @model_validator(mode='after')
    def passwords_must_be_different(self) -> Self:
        if self.old_password == self.new_password:
            raise ValueError("La nueva contraseña no puede ser igual a la anterior")
        return self

class LoginUserDTO(BaseModel):
    email: EmailStr
    password: str

class UserResponseDTO(UserBaseDTO):
    id: str

    model_config = ConfigDict(from_attributes=True)

    
    