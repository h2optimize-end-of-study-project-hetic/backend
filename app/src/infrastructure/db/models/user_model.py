from datetime import datetime
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, TIMESTAMP, text, Enum as PgEnum
from app.src.domain.entities.role import Role


class UserModel(SQLModel, table=True):
    __tablename__ = "user"

    id: int | None = Field(default=None, primary_key=True)

    email: str = Field(..., unique=True, nullable=False)
    salt: str | None = Field(..., nullable=True)
    password: str = Field(..., nullable=False)
    secret_2fa: str | None = Field(default=None)

    role: Role = Field(
        sa_column=Column(
            PgEnum(Role, name="role", create_type=False),
            server_default=Role.guest.value,
            nullable=False
        )
    )

    firstname: str = Field(..., nullable=False)
    lastname: str = Field(..., nullable=False)
    phone_number: str | None = Field(default=None)
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

    updated_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=True,
        ),
    )

    deleted_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=True,
        ),
    )