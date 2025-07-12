from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class TagModel(SQLModel, table=True):
    __tablename__ = "tag"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    test: str
    description: Optional[str] = None
    source_address: str = Field(unique=True)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None