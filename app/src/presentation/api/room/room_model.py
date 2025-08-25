from datetime import datetime

from pydantic import BaseModel, Field

from app.src.presentation.api.common.generic_model import OffsetBasePaginationMetadataModel


class RoomBaseModel(BaseModel):
    name: str = Field(
        ...,
        min_length=3,
        max_length=255,
        title="Room name",
        description="The name must be between 3 and 255 characters long",
    )
    description: str | None = Field(
        default=None,
        title="Room description",
        description="Optional description of the room",
    )
    floor: int | None = Field(default=None, title="Floor", description="Floor number where the room is located")
    building_id: int = Field(default=1, title="Building ID", description="Identifier of the building")
    area: float| None  = Field(default=None, gt=0, title="Area", description="Area of the room in square meters")
    shape: list[list[float]] | None  = Field(default=None, title="Shape", description="List of coordinates representing the shape of the room"
    )
    capacity: int | None  = Field(default=None, ge=0, title="Capacity", description="Maximum number of people allowed")


class RoomCreateModelRequest(RoomBaseModel):
    start_at: datetime | None = Field(..., title="Start availability", description="When the room is available from")
    end_at: datetime | None = Field(default=None, title="End availability", description="When the room is available until")


class RoomUpdateModelRequest(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=3,
        max_length=255,
        title="Room name",
        description="The name must be between 3 and 255 characters long",
    )
    description: str | None = Field(
        default=None, title="Room description", description="Optional description of the room"
    )
    floor: int | None = Field(default=None, title="Floor", description="Floor number where the room is located")
    building_id: int | None = Field(default=None, title="Building ID", description="Identifier of the building")
    area: float | None = Field(default=None, gt=0, title="Area", description="Area of the room in square meters")
    shape: list[list[float]] | None = Field(
        default=None, title="Shape", description="List of coordinates representing the shape of the room"
    )
    capacity: int | None = Field(default=None, ge=1, title="Capacity", description="Maximum number of people allowed")
    start_at: datetime | None = Field(default=None, title="Start availability", description="When the room is available from")
    end_at: datetime | None = Field(default=None, title="End availability", description="When the room is available until")


class RoomModelResponse(RoomBaseModel):
    id: int
    start_at: datetime | None = None
    end_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class PaginatedListRoomModelResponse(BaseModel):
    data: list[RoomModelResponse]
    metadata: OffsetBasePaginationMetadataModel