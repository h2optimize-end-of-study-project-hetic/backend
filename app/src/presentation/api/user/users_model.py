
from pydantic import BaseModel, EmailStr, Field

from app.src.domain.entities.role import Role


class UserBaseModel(BaseModel):
    email: EmailStr = Field(..., min_length=5, max_length=255)
    firstname: str = Field(..., min_length=1, max_length=255)
    lastname: str = Field(..., min_length=1, max_length=255)
    phone_number: str | None = None
    role: Role = Role.guest.value
    is_active: bool = True

class UserCreateModel(UserBaseModel):
    password: str = Field(default="1234", min_length=3)
    salt: str | None = Field(default="1234")
    secret_2fa: str | None = None

class UserUpdateModel(BaseModel):
    email: str | None = Field(default=None, min_length=5, max_length=255)
    firstname: str | None = Field(default=None, min_length=1, max_length=255)
    lastname: str | None = Field(default=None, min_length=1, max_length=255)
    phone_number: str | None = None
    role: Role | None = None
    is_active: bool | None = None
    password: str | None = Field(default=None, min_length=6)
    salt: str | None = None
    secret_2fa: str | None = None

class UserBaseModelResponse(BaseModel):
    id: int
    email: str = Field(..., min_length=5, max_length=255)
    firstname: str = Field(..., min_length=1, max_length=255)
    lastname: str = Field(..., min_length=1, max_length=255)
    phone_number: str | None = None
    role: Role = Role.guest.value
    is_active: bool = True

class UserModel(UserBaseModel):
    id: int

class PaginatedUsersModel(BaseModel):
    data: list[UserBaseModelResponse]
    count: int
    offset: int
    limit: int