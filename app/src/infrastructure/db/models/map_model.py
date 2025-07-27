from datetime import datetime

from sqlalchemy import text
from sqlmodel import Field, SQLModel


class MapModel(SQLModel, table=True):
    __tablename__ = "map"

    id: int | None = Field(default=None, primary_key=True)
    building_id: int |None = Field(default=None)
    filename: str | None = Field(default=None)
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