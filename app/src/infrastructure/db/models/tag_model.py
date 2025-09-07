from datetime import datetime
from sqlalchemy import Column, TIMESTAMP, text
from sqlmodel import Relationship, SQLModel, Field


class TagModel(SQLModel, table=True):
    __tablename__ = "tag"

    id: int | None = Field(default=None, primary_key=True)
    name: str | None = Field(default=None)
    description: str | None = Field(default=None)
    source_address: str = Field(..., unique=True, nullable=False)

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
    room_tags: list["RoomTagModel"] = Relationship(back_populates="tag")
