from datetime import datetime
from pydantic import BaseModel

from app.src.domain.entities.role import Role

class Token(BaseModel):
    access_token: str
    token_type: str

class UserModelResponse(BaseModel):
    id: int
    email: str
    firstname: str
    lastname: str
    phone_number: str | None = None
    role: Role = Role.guest.value
    is_active: bool
    is_delete: bool
    created_at: datetime
    updated_at: datetime | None = None
    deleted_at: datetime | None = None    
