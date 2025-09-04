from datetime import datetime

from sqlalchemy import text
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, TIMESTAMP, text


class EventModel(SQLModel, table=True):
    __tablename__ = "event"

    id: int | None = Field(default=None, primary_key=True)
    name: str | None = Field(default=None)
    description: str | None = Field(default=None)
    group_id: int | None = Field(default=None)
    supervisor: int | None = Field(default=None)
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