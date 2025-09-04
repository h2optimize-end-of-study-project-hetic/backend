from datetime import datetime

from sqlalchemy import text
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, TIMESTAMP, JSON, text


class MapModel(SQLModel, table=True):
    __tablename__ = "map"

    id: int | None = Field(default=None, primary_key=True)
    building_id: int |None = Field(default=None)
    file_name: str | None = Field(default=None)
    floor: int | None = Field(default=None)
    path: str | None = Field(default=None)
    width: int | None = Field(default=None)
    length: int | None = Field(default=None)
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