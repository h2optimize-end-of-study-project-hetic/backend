from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, TIMESTAMP, DECIMAL, text


class BuildingModel(SQLModel, table=True):
    __tablename__ = "building"

    id: int | None = Field(default=None, primary_key=True)

    name: str | None = Field(default=None)
    description: str | None = Field(default=None)
    room_count: int | None = Field(default=None)
    street_number: str | None = Field(default=None)
    street_name: str | None = Field(default=None)
    postal_code: str | None = Field(default=None)
    city: str | None = Field(default=None)
    country: str | None = Field(default=None)

    latitude: float | None = Field(
        default=None,
        sa_column=Column(DECIMAL(9, 6), nullable=True),
    )
    longitude: float | None = Field(
        default=None,
        sa_column=Column(DECIMAL(9, 6), nullable=True),
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
    
    rooms: list['RoomModel'] = Relationship(back_populates="building")
