from datetime import datetime

from pydantic import BaseModel, Field


class TagsBaseModel(BaseModel):
    name: str = Field(
        ...,
        min_length=3,
        max_length=255,
        title="Tag name",
        description="The name must be between 3 and 255 characters long",
    )
    source_address: str = Field(
        ..., min_length=3, title="Source address", description="The source address must be at least 3 characters long"
    )
    description: str | None = Field(
        default=None, title="Tag description", description="Optional description of the tag"
    )


class TagsCreateModel(TagsBaseModel):
    room_id: int | None = Field(
        default=None,
        ge=1,
        title="Associated room",
        description="Optional ID of the room associated with the tag (positive integer)",
    )


class TagsModel(TagsBaseModel):
    id: int
    created_at: datetime | None
    updated_at: datetime | None


class TagsUpdateModel(BaseModel):
    name: str | None = Field(default=None, min_length=3, max_length=255)
    source_address: str | None = Field(default=None, min_length=3)
    description: str | None = None


class PaginationMetadataModel(BaseModel):
    total: int = Field(..., ge=0, description="Total number of elements in the collection")
    chunk_size: int = Field(..., ge=1, description="Number of elements returned in the current chunk")
    chunk_count: int = Field(..., ge=1, description="Total number of chunks available")
    current_cursor: str | None = Field(None, description="Cursor of the current chunk")
    first_cursor: str | None = Field(None, description="Cursor of the first chunk")
    last_cursor: str | None = Field(None, description="Cursor of the last chunk")
    next_cursor: str | None = Field(None, description="Cursor to fetch the next chunk, if any")


class PaginatedModel(BaseModel):
    data: list[TagsModel]
    metadata: PaginationMetadataModel
