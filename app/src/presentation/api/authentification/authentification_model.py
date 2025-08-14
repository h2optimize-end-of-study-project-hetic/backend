from datetime import datetime
from typing import Optional
from app.src.infrastructure.db.models.user_model import RoleEnum
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

# class User(BaseModel):
#     id: int
#     firstname: str
#     lastname: str
#     email: str
#     role: str
#     disabled: bool

class UserInDB(User):
    hashed_password: str

class User(BaseModel):
    id: int
    email: str
    firstname: str
    lastname: str
    phone_number: Optional[str] = None
    role: RoleEnum
    is_active: bool
    is_delete: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    password: Optional[str] = None
    salt: Optional[str] = None


    class Config:
        from_attributes = True  # permet de créer à partir d'un SQLModel/ORM