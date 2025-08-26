from typing import Optional, List
from pydantic import BaseModel, Field
from app.src.domain.entities.role import Role

class UserBaseModel(BaseModel):
    email: str = Field(..., min_length=5, max_length=255)
    firstname: str = Field(..., min_length=1, max_length=255)
    lastname: str = Field(..., min_length=1, max_length=255)
    phone_number: Optional[str] = None
    role: Role = Role.GUEST
    is_active: bool = True

class UserCreateModel(UserBaseModel):
    password: str = Field(..., min_length=6)
    salt: str
    secret_2fa: Optional[str] = None

class UserUpdateModel(BaseModel):
    email: Optional[str] = Field(default=None, min_length=5, max_length=255)
    firstname: Optional[str] = Field(default=None, min_length=1, max_length=255)
    lastname: Optional[str] = Field(default=None, min_length=1, max_length=255)
    phone_number: Optional[str] = None
    role: Optional[Role] = None
    is_active: Optional[bool] = None
    password: Optional[str] = Field(default=None, min_length=6)
    salt: Optional[str] = None
    secret_2fa: Optional[str] = None

class UserModel(UserBaseModel):
    id: int

class PaginatedUsersModel(BaseModel):
    data: List[UserModel]
    count: int
    offset: int
    limit: int