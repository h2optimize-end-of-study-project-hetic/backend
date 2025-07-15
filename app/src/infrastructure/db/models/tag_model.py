from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class TagModel(SQLModel, table=True):
    __tablename__ = "tag"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    source_address: Optional[str] = Field(default=None, unique=True)
    created_at: Optional[datetime] = Field(default=None, nullable=True, sa_column_kwargs={"server_default": "CURRENT_TIMESTAMP"})
    updated_at: Optional[datetime] = Field(default=None, nullable=True)