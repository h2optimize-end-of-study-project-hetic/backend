from datetime import datetime

from sqlmodel import Field, SQLModel


class TagModel(SQLModel, table=True):
    __tablename__ = "tag"

    id: int | None = Field(default=None, primary_key=True)
    name: str | None = Field(default=None)
    description: str | None = Field(default=None)
    source_address: str | None = Field(default=None, unique=True)
    created_at: datetime | None = Field(
        default=None, nullable=True, sa_column_kwargs={"server_default": "CURRENT_TIMESTAMP"}
    )
    updated_at: datetime | None = Field(default=None, nullable=True)
