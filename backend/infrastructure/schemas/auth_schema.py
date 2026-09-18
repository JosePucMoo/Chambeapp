from pydantic import BaseModel, EmailStr, Field, model_validator
from typing_extensions import Self

class RegisterDTO(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, description="Mínimo 8 caracteres")
    confirm_password: str = Field(..., min_length=8, description="Mínimo 8 caracteres")

    @model_validator(mode='after')
    def check_passwords_match(self) -> Self:
        if self.password != self.confirm_password:
            raise ValueError("Las contraseñas no coinciden")
        return self

class LoginDTO(BaseModel):
    email: EmailStr
    password: str

class ForgotPasswordDTO(BaseModel):
    email: EmailStr

class ResetPasswordDTO(BaseModel):
    token: str = Field(..., description="Token recibido por correo")
    new_password: str = Field(..., min_length=8)
    confirm_password: str

    @model_validator(mode='after')
    def check_passwords_match(self) -> Self:
        if self.new_password != self.confirm_password:
            raise ValueError("Las contraseñas no coinciden")
        return self

class RegisterResponseDTO(BaseModel):
    message: str
    email: str