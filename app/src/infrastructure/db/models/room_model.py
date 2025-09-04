from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, TIMESTAMP, JSON, text


class RoomModel(SQLModel, table=True):
    __tablename__ = "room"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(..., nullable=False)
    description: str | None = Field(default=None)
    floor: int = Field(..., nullable=True)
    building_id: int = Field(..., foreign_key="building.id", nullable=False)
    area: float | None = Field(default=None, nullable=True)
    shape: list[list[float]] | None = Field(default=None, sa_column=Column(JSON, nullable=True))
    capacity: int | None = Field(default=None, nullable=True)

    start_at: datetime| None = Field(
        default=None,
        sa_column=Column(TIMESTAMP(timezone=True), nullable=False),
    )
    end_at: datetime | None = Field(
        default=None,
        sa_column=Column(TIMESTAMP(timezone=True), nullable=True),
    )
    created_at: datetime | None = Field(
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
    building: 'BuildingModel' = Relationship(back_populates="rooms")
