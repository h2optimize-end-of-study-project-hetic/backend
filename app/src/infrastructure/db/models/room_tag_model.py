
from datetime import datetime
from sqlalchemy import TIMESTAMP, Column, text
from sqlmodel import Field, Relationship, SQLModel


class RoomTagModel(SQLModel, table=True):
    __tablename__ = "room_tag"

    id: int | None = Field(default=None, primary_key=True)
    tag_id: int = Field(foreign_key="tag.id", nullable=False)
    room_id: int = Field(foreign_key="room.id", nullable=False)

    start_at: datetime | None = Field(
        default=None,
        sa_column=Column(TIMESTAMP(timezone=True), nullable=True),
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
        )
    )
    updated_at: datetime | None = Field(
        default=None,
        sa_column=Column(TIMESTAMP(timezone=True), nullable=True),
    )

    tag: "TagModel" = Relationship(back_populates="room_tags")
    room: "RoomModel" = Relationship(back_populates="tags")