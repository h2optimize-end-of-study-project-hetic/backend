from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, TIMESTAMP, text, Enum as PgEnum
import enum

class RoleEnum(str, enum.Enum):
    admin = "admin"
    staff = "staff"
    technician = "technician"
    intern = "intern"
    guest = "guest"

class UserModel(SQLModel, table=True):
    tablename = "user"

    id: Optional[int] = Field(default=None, primary_key=True)

    email: str = Field(..., unique=True, nullable=False)
    salt: str = Field(..., nullable=False)
    password: str = Field(..., nullable=False)
    secret_2fa: Optional[str] = Field(default=None)

    role: RoleEnum = Field(
        sa_column=Column(
            PgEnum(RoleEnum, name="role", create_type=False),
            server_default="guest",
            nullable=False
        )
    )

    firstname: str = Field(..., nullable=False)
    lastname: str = Field(..., nullable=False)
    phone_number: Optional[str] = Field(default=None)
    is_active: bool = Field(default=True, nullable=False)
    is_delete: bool = Field(default=False, nullable=False)

    created_at: datetime = Field(
        default=None,
        sa_column=Column(
            TIMESTAMP(timezone=True),
            server_default=text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
    )

    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=True,
        ),
    )

    deleted_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=True,
        ),
    )