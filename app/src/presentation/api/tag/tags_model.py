from datetime import datetime
from typing import List
from typing import Optional
from pydantic import BaseModel, Field


class TagsBaseModel(BaseModel):
    name: str = Field(..., min_length=3,max_length=255,  title="Tag name", description="The name must be between 3 and 255 characters long")
    source_address: str = Field(..., min_length=3, title="Source address", description="The source address must be at least 3 characters long" )
    description: Optional[str] = Field(default=None, title="Tag description", description="Optional description of the tag")

class TagsCreateModel(TagsBaseModel):
    room_id: Optional[int] = Field(default=None, ge=1, title="Associated room", description="Optional ID of the room associated with the tag (positive integer)")

class TagsModel(TagsBaseModel):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

class TagsUpdateModel(BaseModel):
    name: Optional[str] = Field(default=None, min_length=3, max_length=255)
    source_address: Optional[str] = Field(default=None, min_length=3)
    description: Optional[str] = None


class PaginationMetadataModel(BaseModel):
    total: int = Field(..., ge=0, description="Total number of elements in the collection")
    chunk_size: int = Field(..., ge=1, description="Number of elements returned in the current chunk")
    chunk_count: int = Field(..., ge=1, description="Total number of chunks available")
    current_cursor: Optional[str] = Field(None, description="Cursor of the current chunk")
    first_cursor: Optional[str] = Field(None, description="Cursor of the first chunk")
    last_cursor: Optional[str] = Field(None, description="Cursor of the last chunk")
    next_cursor: Optional[str] = Field(None, description="Cursor to fetch the next chunk, if any")

class PaginatedModel(BaseModel):
    data: List[TagsModel]
    metadata: PaginationMetadataModel