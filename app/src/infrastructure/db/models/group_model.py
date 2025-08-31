from datetime import datetime

from sqlalchemy import text
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, TIMESTAMP, text


class GroupModel(SQLModel, table=True):
    __tablename__ = "group"

    id: int | None = Field(default=None, primary_key=True)

    name: str |None = Field(default=None)
    description: str | None = Field(default=None)
    member_count: int | None = Field(default=None)

    start_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=True,
        ),
    )
    end_at: datetime | None = Field(
        default=None,
        sa_column=Column(
            TIMESTAMP(timezone=True),
            nullable=True,
        ),
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