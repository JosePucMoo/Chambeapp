from pydantic import EmailStr, Field, model_validator
from typing_extensions import Self

from infrastructure.schemas.base_schema import BaseSchema


class RegisterDTO(BaseSchema):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, description="Mínimo 8 caracteres")
    confirm_password: str = Field(..., min_length=8, description="Mínimo 8 caracteres")

    @model_validator(mode="after")
    def check_passwords_match(self) -> Self:
        if self.password != self.confirm_password:
            raise ValueError("Las contraseñas no coinciden")
        return self


class LoginRequestDTO(BaseSchema):
    email: EmailStr
    password: str


class ForgotPasswordDTO(BaseSchema):
    email: EmailStr


class ResetPasswordDTO(BaseSchema):
    new_password: str = Field(..., min_length=8)
    confirm_password: str

    @model_validator(mode="after")
    def check_passwords_match(self) -> Self:
        if self.new_password != self.confirm_password:
            raise ValueError("Las contraseñas no coinciden")
        return self


class UserResponseDTO(BaseSchema):
    id: str
    name: str
    email: EmailStr


class LoginResponseDTO(BaseSchema):
    token: str
    user: UserResponseDTO
