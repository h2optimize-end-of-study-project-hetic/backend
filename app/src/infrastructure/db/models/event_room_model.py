from datetime import datetime

from sqlalchemy import text
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, TIMESTAMP, JSON, text


class EventRoomModel(SQLModel, table=True):
    __tablename__ = "event_room"

    id: int | None = Field(default=None, primary_key=True)
    room_id: int |None = Field(default=None)
    event_id: int | None = Field(default=None)
    is_finished: bool | None = Field(default=None)
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