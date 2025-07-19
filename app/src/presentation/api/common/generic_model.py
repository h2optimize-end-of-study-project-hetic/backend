from pydantic import BaseModel, Field


class PaginationMetadataModel(BaseModel):
    total: int = Field(..., ge=0, description="Total number of elements in the collection")
    chunk_size: int = Field(..., ge=0, description="Number of elements returned in the current chunk")
    chunk_count: int = Field(..., ge=0, description="Total number of chunks available")
    current_cursor: str | None = Field(None, description="Cursor of the current chunk")
    first_cursor: str | None = Field(None, description="Cursor of the first chunk")
    last_cursor: str | None = Field(None, description="Cursor of the last chunk")
    next_cursor: str | None = Field(None, description="Cursor to fetch the next chunk, if any")
