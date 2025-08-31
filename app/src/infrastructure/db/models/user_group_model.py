from datetime import datetime

from sqlalchemy import text
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, TIMESTAMP, text, Integer, ForeignKey


class UserGroupModel(SQLModel, table=True):
    __tablename__ = "user_group"

    user_id: int = Field(
        sa_column=Column(Integer, ForeignKey("user.id"), primary_key=True)
    )
    group_id: int = Field(
        sa_column=Column(Integer, ForeignKey("group.id"), primary_key=True)
    )

    created_at: datetime | None = Field(
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