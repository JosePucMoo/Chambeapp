from pydantic import EmailStr

from infrastructure.schemas.base_schema import BaseSchema


class InviteMemberDTO(BaseSchema):
    email: EmailStr
