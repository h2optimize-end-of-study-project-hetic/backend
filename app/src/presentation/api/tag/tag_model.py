from datetime import datetime

from pydantic import BaseModel, Field

from app.src.presentation.api.common.generic_model import PaginationMetadataModel


class TagBaseModel(BaseModel):
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


class TagCreateModelRequest(TagBaseModel):
    pass


class TagUpdateModelRequest(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=3,
        max_length=255,
        title="Tag name",
        description="The name must be between 3 and 255 characters long",
    )
    source_address: str | None = Field(
        default=None,
        min_length=3,
        title="Source address",
        description="The source address must be at least 3 characters long",
    )
    description: str | None = Field(
        default=None, title="Tag description", description="Optional description of the tag"
    )


class TagModelResponse(TagBaseModel):
    id: int
    created_at: datetime | None
    updated_at: datetime | None


class PaginatedListTagModelResponse(BaseModel):
    data: list[TagModelResponse]
    metadata: PaginationMetadataModel
