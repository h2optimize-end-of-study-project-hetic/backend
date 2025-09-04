from datetime import datetime

from pydantic import BaseModel, Field

from app.src.presentation.api.common.generic_model import PaginationMetadataModel


class MapBaseModel(BaseModel):
    building_id: int = Field (
        default=None, title="Building ID", description="The building ID to which this map is attached to"
    )
    file_name: str = Field(
        ...,
        min_length=3,
        max_length=255,
        title="File_name",
        description="The file_name must be between 3 and 255 characters long : 'Building name - Floor'",
    )
    floor: int = Field(
        title="Floor",
        description="Floor of the building"
    )
    path: str = Field(
        ..., min_length=3, title="Pathfile", description="The path must be at least 3 characters long"
    )
    width: int = Field(
        default=None, title="Width of the map", description="Width"
    )
    length: int = Field(
        default=None, title="Length of the map", description="Length"
    )


class MapCreateModelRequest(MapBaseModel):
    pass


class MapUpdateModelRequest(BaseModel):
    building_id: int | None = Field (
        default=None, 
        title="Building ID", 
        description="The building ID to which this map is attached to"
    )
    floor: int | None = Field (
        default=None, 
        title="Floor", 
        description="The floor of the building"
    )


class MapModelResponse(MapBaseModel):
    id: int
    created_at: datetime | None
    updated_at: datetime | None


class PaginatedListMapModelResponse(BaseModel):
    data: list[MapModelResponse]
    metadata: PaginationMetadataModel
