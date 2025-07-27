from datetime import datetime
from sqlmodel import SQLModel, Field
from sqlalchemy import Column, TIMESTAMP, JSON, text


class RoomModel(SQLModel, table=True):
    __tablename__ = "room"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(..., nullable=False)
    description: str | None = Field(default=None)
    floor: int = Field(..., nullable=False)
    building_id: int = Field(..., foreign_key="building.id", nullable=False)
    area: float = Field(..., nullable=False)
    shape: list[list[float]] = Field(..., sa_column=Column(JSON, nullable=False))
    capacity: int = Field(..., nullable=False)

    start_at: datetime | None = Field(
        default=None,
        sa_column=Column(TIMESTAMP(timezone=True), nullable=True),
    )
    end_at: datetime | None = Field(
        default=None,
        sa_column=Column(TIMESTAMP(timezone=True), nullable=True),
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
