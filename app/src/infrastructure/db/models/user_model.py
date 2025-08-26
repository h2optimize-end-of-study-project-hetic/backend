from datetime import datetime

from app.src.domain.entities.role import Role
from sqlalchemy import text
from sqlmodel import Field, SQLModel

class UserModel(SQLModel, table=True):
    __tablename__ = "user"

    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    password: str
    salt: str
    secret_2fa: str | None = Field(default=None)
    firstname: str
    lastname: str
    role: str = Field(default=Role.GUEST)
    phone_number: str | None = Field(default=None)
    is_active: bool = Field(default=True)
    is_delete: bool = Field(default=False)
    created_at: datetime | None = Field(default=None, nullable=True, sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP")})
    updated_at: datetime | None = Field(default=None, nullable=True)
    deleted_at: datetime | None = Field(default=None, nullable=True)