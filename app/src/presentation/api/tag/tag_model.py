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

class TagCreateWithRoomLinkModelRequest(TagBaseModel):
    room_id: int = Field(..., ge=1, title="Room ID", description="Identifier of the room")
    start_at: datetime | None = Field(default=None, title="Start availability")
    end_at: datetime | None = Field(default=None, title="End availability")


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

class TagUpdateWithRoomLinkModelRequest(TagUpdateModelRequest):
    room_id: int | None = Field(default=None, title="Room ID", description="Room to link or unlink")
    start_at: datetime | None = Field(default=None, title="Start availability")
    end_at: datetime | None = Field(default=None, title="End availability")

class Building(BaseModel):
    id: int
    name: str = Field (default=None, title="Name", description="The name of the building")
    description: str = Field (default=None, title="Description", description="The description of the building")
    created_at: datetime | None
    updated_at: datetime | None

class Room(BaseModel) :
    id: int
    name: str = Field(..., min_length=3,max_length=255,title="Room name",description="The name must be between 3 and 255 characters long",)
    description: str | None = Field(default=None, title="Room description", description="Optional description of the room")
    building_id: int | None = None 
    building: Building
    start_at: datetime | None = None
    end_at: datetime | None = None
    floor: int | None = Field(default=None, title="Floor", description="Floor number where the room is located")
    created_at: datetime | None = None
    updated_at: datetime | None = None

class LinkRoomTag(BaseModel):
    id: int
    room: Room
    start_at: datetime | None = Field(default=None, title="Start availability", description="When the room is available from")
    end_at: datetime | None = Field(default=None, title="End availability", description="When the room is available until")
    created_at: datetime | None
    updated_at: datetime | None


class TagModelResponse(TagBaseModel):
    id: int
    created_at: datetime | None
    updated_at: datetime | None
    rooms: list[LinkRoomTag] | None = None 

class PaginatedListTagModelResponse(BaseModel):
    data: list[TagModelResponse]
    metadata: PaginationMetadataModel
